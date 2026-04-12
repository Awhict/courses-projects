from time import time
import datetime
import os
import pickle
import hashlib as hasher
import acoustic.acoustid_check as ac
import text_compare.test_text as tc
import image_compare.image_check as ic

# 交易类，每个交易包含标题、文件名、作者、公钥、类型和媒体文件信息
class Transaction: 
    # 初始化交易
    def __init__(self, title="", filename="", author="", public_key="", genre="", media = ""):
        self.title = title
        self.filename = filename
        self.author = author
        self.public_key = public_key
        self.genre = genre
        self.media = media

    # 将交易转换为字典形式
    def toDict(self):
        return {
            'title': self.title,
            'filename': self.filename,
            'author': self.author,
            'public_key': self.public_key,
            'genre': self.genre,
            'media': self.media,
    }

    # 定义交易的字符串表示形式
    def __str__(self):
        toString = self.author + " : " + self.genre + " (" + self.media + ") "
        return toString;


# 区块类，每个区块包含索引、时间戳、前一个区块的哈希值和交易信息
class Block:
    def __init__(self, index, transaction, previous_hash):
        self.index = index
        self.timestamp = time()
        self.previous_hash = previous_hash
        self.transaction = transaction
    
    # 计算区块的哈希值
    def compute_hash(self):
        concat_str = str(self.index) + str(self.timestamp) + str(self.previous_hash) + str(self.transaction['author']) + str(self.transaction['genre'])
        hash_result = hasher.sha256(concat_str.encode('utf-8')).hexdigest()
        return hash_result

    # 序列化区块信息
    def serialize(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'transaction': self.transaction
        }


# 区块链类，包含区块和交易的管理
class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = {}  # 未确认的交易
        self.chain = []  # 区块链

    # 创建创世区块（区块链的第一个区块）
    def create_genesis_block(self):
        empty_media = {
            'title': "",
            'filename': "",
            'author': "",
            'public_key': "",
            'genre': "",
            'media': "",
        }
        new_block = Block(index=0, transaction=empty_media, previous_hash=0)
        self.add_block(new_block)
        return new_block
    
    # 创建新交易
    def new_transaction(self, title, filename, author, public_key, genre, media):
        new_trans = Transaction(title, filename, author, public_key, genre, media).toDict()
        self.unconfirmed_transactions = new_trans.copy()
        return new_trans
    
    # 挖矿，生成新块并验证其合法性后添加到区块链中
    def mine(self):
        if len(self.chain) == 0:
            block_idx = 1
            previous_hash = 0
        else:
            block_idx = self.chain[-1].index + 1
            previous_hash = self.chain[-1].compute_hash()
        block = Block(block_idx, self.unconfirmed_transactions, previous_hash)
        if self.verify_block(block):
            self.add_block(block)
            return block
        else:
            return None
    
    # 验证区块合法性
    def verify_block(self, block):
        # 检查前一个区块的哈希值
        if len(self.chain) == 0:
            previous_hash = 0
        else:
            previous_hash = self.chain[-1].compute_hash()
        if block.previous_hash != previous_hash:
            return 0
        # 检查媒体文件的原创性
        for prev_block in self.chain:
            if block.transaction['genre'] == prev_block.transaction['genre']:
                try:
                    if block.transaction['genre'] == 'Audio':
                        score = ac.calc_accuracy('./uploads/' + block.transaction['media'], './uploads/' + prev_block.transaction['media'])
                        print(score)
                        if score > 0.9:
                            return 0
                    if block.transaction['genre'] == 'Text':
                        score = tc.check_text_similarity('./uploads/' + block.transaction['media'], './uploads/' + prev_block.transaction['media'])
                        print(score)
                        if score < 100:
                            return 0
                    if block.transaction['genre'] == "Image":
                        score = ic.calc_accuracy('./uploads/' + block.transaction['media'], './uploads/' + prev_block.transaction['media'])
                        print(score)
                        if score < 0.4:
                            return 0
                except:
                    return 0
        return 1

    # 查找特定交易的原创性
    def lookup(self, transaction):
        for prev_block in self.chain:
            if transaction['genre'] == prev_block.transaction['genre']:
                try:
                    if transaction['genre'] == 'Audio':
                        score = ac.calc_accuracy('./tmp/' + transaction['media'], './uploads/' + prev_block.transaction['media'])
                        print(score)
                        if score > 0.9:
                            return prev_block
                    if transaction['genre'] == 'Text':
                        score = tc.check_text_similarity('./tmp/' + transaction['media'], './uploads/' + prev_block.transaction['media'])
                        print(score)
                        if score < 100:
                            return prev_block
                    if transaction['genre'] == "Image":
                        score = ic.calc_accuracy('./tmp/' + transaction['media'], './uploads/' + prev_block.transaction['media'])
                        print(score)
                        if score < 0.4:
                            return prev_block
                except:
                    print("exception")
                    return prev_block
        return None
    
    # 将区块添加到区块链中，并将链保存到文件
    def add_block(self, block):
        self.chain.append(block)
        with open('./blockchain/chain.pkl', 'wb') as output:
            pickle.dump(self.chain, output, pickle.HIGHEST_PROTOCOL)

    # 检查区块链的完整性（功能未实现）
    def check_integrity(self):
        return 0

    # 返回区块链的最后一个区块
    @property
    def last_block(self):
        return self.chain[-1]
