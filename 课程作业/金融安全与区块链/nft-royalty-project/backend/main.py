from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import web3
import json
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps

app = Flask(__name__)
CORS(app)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nft_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

db = SQLAlchemy(app)

# 配置Web3
w3 = web3.Web3(web3.HTTPProvider('http://localhost:8545'))  # 本地Ganache网络
if w3.is_connected():
    print("成功连接到以太坊网络")
else:
    print("无法连接到以太坊网络")

# 加载合约ABI和地址
with open('contracts/NFTMarketplace.abi') as f:
    marketplace_abi = json.load(f)

with open('contracts/NFT.abi') as f:
    nft_abi = json.load(f)

MARKETPLACE_ADDRESS = '0xYourMarketplaceContractAddress'
NFT_ADDRESS = '0xYourNFTContractAddress'

marketplace_contract = w3.eth.contract(address=MARKETPLACE_ADDRESS, abi=marketplace_abi)
nft_contract = w3.eth.contract(address=NFT_ADDRESS, abi=nft_abi)

# 模型定义
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    wallet_address = db.Column(db.String(42))
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    nfts = db.relationship('NFT', backref='owner', lazy=True)
    transactions = db.relationship('Transaction', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_token(self):
        payload = {
            'user_id': self.id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return None
        return User.query.get(payload['user_id'])

class NFT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255), nullable=False)
    metadata_url = db.Column(db.String(255))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    royalty = db.Column(db.Float, default=5.0)  # 版税百分比
    is_for_sale = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sold_at = db.Column(db.DateTime)
    collection = db.Column(db.String(100))
    category = db.Column(db.String(50))

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tx_hash = db.Column(db.String(66), nullable=False)
    nft_id = db.Column(db.Integer, db.ForeignKey('nft.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    platform_fee = db.Column(db.Float, nullable=False)
    royalty_fee = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(255))
    cover_url = db.Column(db.String(255))
    social_links = db.Column(db.JSON)  # 存储社交媒体链接的JSON对象

# 身份验证装饰器
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        if not token:
            return jsonify({'message': '身份验证令牌缺失!'}), 401
        try:
            user = User.verify_token(token)
            if not user:
                return jsonify({'message': '无效的令牌!'}), 401
        except:
            return jsonify({'message': '无效的令牌!'}), 401
        return f(user, *args, **kwargs)
    return decorated

# 路由
@app.route('/api/users/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'message': '缺少必要的注册信息!'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': '用户名已存在!'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': '邮箱已被注册!'}), 400
    
    new_user = User(
        username=data['username'],
        email=data['email'],
        wallet_address=data.get('wallet_address')
    )
    new_user.set_password(data['password'])
    
    try:
        db.session.add(new_user)
        db.session.commit()
        
        # 创建用户资料
        profile = UserProfile(
            user_id=new_user.id,
            bio='',
            avatar_url='https://picsum.photos/200/200',
            cover_url='https://picsum.photos/800/300',
            social_links={}
        )
        db.session.add(profile)
        db.session.commit()
        
        return jsonify({
            'message': '注册成功!',
            'user': {
                'id': new_user.id,
                'username': new_user.username,
                'email': new_user.email,
                'wallet_address': new_user.wallet_address,
                'created_at': new_user.created_at.strftime('%Y-%m-%d %H:%M:%S')
            },
            'token': new_user.generate_token()
        }), 201
    except:
        db.session.rollback()
        return jsonify({'message': '注册失败，请重试!'}), 500

@app.route('/api/users/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'message': '缺少必要的登录信息!'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'message': '邮箱或密码错误!'}), 401
    
    return jsonify({
        'message': '登录成功!',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'wallet_address': user.wallet_address,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
        },
        'token': user.generate_token()
    }), 200

@app.route('/api/nfts', methods=['GET'])
def get_nfts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    category = request.args.get('category')
    sort = request.args.get('sort', 'newest')  # newest, oldest, price_high, price_low
    
    query = NFT.query.filter_by(is_for_sale=True)
    
    if category:
        query = query.filter_by(category=category)
    
    if sort == 'newest':
        query = query.order_by(NFT.created_at.desc())
    elif sort == 'oldest':
        query = query.order_by(NFT.created_at.asc())
    elif sort == 'price_high':
        query = query.order_by(NFT.price.desc())
    elif sort == 'price_low':
        query = query.order_by(NFT.price.asc())
    
    nfts = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'nfts': [{
            'id': nft.id,
            'token_id': nft.token_id,
            'name': nft.name,
            'description': nft.description,
            'image_url': nft.image_url,
            'creator': {
                'id': nft.creator_id,
                'username': User.query.get(nft.creator_id).username if User.query.get(nft.creator_id) else '未知'
            },
            'owner': {
                'id': nft.owner_id,
                'username': User.query.get(nft.owner_id).username if User.query.get(nft.owner_id) else '未知'
            },
            'price': nft.price,
            'royalty': nft.royalty,
            'created_at': nft.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'collection': nft.collection,
            'category': nft.category
        } for nft in nfts.items],
        'total': nfts.total,
        'pages': nfts.pages,
        'current_page': page
    }), 200

@app.route('/api/nfts/<int:nft_id>', methods=['GET'])
def get_nft(nft_id):
    nft = NFT.query.get(nft_id)
    
    if not nft:
        return jsonify({'message': 'NFT不存在!'}), 404
    
    return jsonify({
        'id': nft.id,
        'token_id': nft.token_id,
        'name': nft.name,
        'description': nft.description,
        'image_url': nft.image_url,
        'metadata_url': nft.metadata_url,
        'creator': {
            'id': nft.creator_id,
            'username': User.query.get(nft.creator_id).username if User.query.get(nft.creator_id) else '未知',
            'profile': {
                'avatar_url': UserProfile.query.filter_by(user_id=nft.creator_id).first().avatar_url if UserProfile.query.filter_by(user_id=nft.creator_id).first() else ''
            }
        },
        'owner': {
            'id': nft.owner_id,
            'username': User.query.get(nft.owner_id).username if User.query.get(nft.owner_id) else '未知',
            'profile': {
                'avatar_url': UserProfile.query.filter_by(user_id=nft.owner_id).first().avatar_url if UserProfile.query.filter_by(user_id=nft.owner_id).first() else ''
            }
        },
        'price': nft.price,
        'royalty': nft.royalty,
        'is_for_sale': nft.is_for_sale,
        'created_at': nft.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'sold_at': nft.sold_at.strftime('%Y-%m-%d %H:%M:%S') if nft.sold_at else None,
        'collection': nft.collection,
        'category': nft.category,
        'transactions': [{
            'id': tx.id,
            'tx_hash': tx.tx_hash,
            'buyer': {
                'id': tx.buyer_id,
                'username': User.query.get(tx.buyer_id).username if User.query.get(tx.buyer_id) else '未知'
            },
            'seller_id': tx.seller_id,
            'price': tx.price,
            'platform_fee': tx.platform_fee,
            'royalty_fee': tx.royalty_fee,
            'timestamp': tx.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'status': tx.status
        } for tx in Transaction.query.filter_by(nft_id=nft_id).order_by(Transaction.timestamp.desc()).all()]
    }), 200

@app.route('/api/nfts/create', methods=['POST'])
@token_required
def create_nft(current_user):
    data = request.get_json()
    
    if not data or 'name' not in data or 'image_url' not in data or 'price' not in data:
        return jsonify({'message': '缺少必要的NFT信息!'}), 400
    
    # 生成元数据URL
    metadata = {
        'name': data['name'],
        'description': data.get('description', ''),
        'image': data['image_url'],
        'attributes': data.get('attributes', []),
        'creator': current_user.username,
        'royalty': data.get('royalty', 5.0)
    }
    
    # 在实际应用中，元数据应该存储在IPFS或其他存储服务上
    metadata_url = f"https://example.com/metadata/{data['name'].replace(' ', '_')}_{current_user.id}_{datetime.now().timestamp()}.json"
    
    # 铸造NFT
    try:
        # 这里应该调用智能合约的铸造函数
        # token_id = nft_contract.functions.mint(current_user.wallet_address, metadata_url).transact({
        #     'from': w3.eth.accounts[0],  # 管理员账户
        #     'gas': 500000
        # })
        
        # 模拟token_id
        token_id = len(NFT.query.all()) + 1
        
        new_nft = NFT(
            token_id=token_id,
            name=data['name'],
            description=data.get('description', ''),
            image_url=data['image_url'],
            metadata_url=metadata_url,
            creator_id=current_user.id,
            owner_id=current_user.id,
            price=data['price'],
            royalty=data.get('royalty', 5.0),
            is_for_sale=data.get('is_for_sale', True),
            collection=data.get('collection'),
            category=data.get('category')
        )
        
        db.session.add(new_nft)
        db.session.commit()
        
        return jsonify({
            'message': 'NFT创建成功!',
            'nft': {
                'id': new_nft.id,
                'token_id': new_nft.token_id,
                'name': new_nft.name,
                'description': new_nft.description,
                'image_url': new_nft.image_url,
                'metadata_url': new_nft.metadata_url,
                'creator_id': new_nft.creator_id,
                'owner_id': new_nft.owner_id,
                'price': new_nft.price,
                'royalty': new_nft.royalty,
                'is_for_sale': new_nft.is_for_sale,
                'created_at': new_nft.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'collection': new_nft.collection,
                'category': new_nft.category
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'NFT创建失败: {str(e)}'}), 500

@app.route('/api/nfts/<int:nft_id>/buy', methods=['POST'])
@token_required
def buy_nft(current_user, nft_id):
    data = request.get_json()
    
    if not data or 'wallet_address' not in data or 'signature' not in data:
        return jsonify({'message': '缺少必要的购买信息!'}), 400
    
    nft = NFT.query.get(nft_id)
    
    if not nft:
        return jsonify({'message': 'NFT不存在!'}), 404
    
    if not nft.is_for_sale:
        return jsonify({'message': '此NFT不售卖!'}), 400
    
    if current_user.id == nft.owner_id:
        return jsonify({'message': '您已经是此NFT的所有者!'}), 400
    
    # 平台费用 2%
    platform_fee = nft.price * 0.02
    
    # 版税费用
    royalty_fee = 0
    if nft.creator_id != nft.owner_id:  # 如果创作者不是当前卖家
        royalty_fee = nft.price * (nft.royalty / 100)
    
    # 卖家实际收入
    seller_revenue = nft.price - platform_fee - royalty_fee
    
    try:
        # 这里应该调用智能合约的购买函数
        # tx_hash = marketplace_contract.functions.buyNFT(nft.token_id).transact({
        #     'from': data['wallet_address'],
        #     'value': w3.to_wei(nft.price, 'ether'),
        #     'gas': 500000
        # })
        
        # 模拟交易哈希
        tx_hash = f"0x{os.urandom(32).hex()}"
        
        # 创建交易记录
        transaction = Transaction(
            tx_hash=tx_hash,
            nft_id=nft.id,
            buyer_id=current_user.id,
            seller_id=nft.owner_id,
            price=nft.price,
            platform_fee=platform_fee,
            royalty_fee=royalty_fee,
            status='completed'
        )
        
        # 更新NFT所有权
        nft.owner_id = current_user.id
        nft.is_for_sale = False
        nft.sold_at = datetime.utcnow()
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'message': '购买成功!',
            'transaction': {
                'id': transaction.id,
                'tx_hash': transaction.tx_hash,
                'nft_id': transaction.nft_id,
                'buyer_id': transaction.buyer_id,
                'seller_id': transaction.seller_id,
                'price': transaction.price,
                'platform_fee': transaction.platform_fee,
                'royalty_fee': transaction.royalty_fee,
                'timestamp': transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'status': transaction.status
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'购买失败: {str(e)}'}), 500

@app.route('/api/users/<int:user_id>/profile', methods=['GET'])
def get_user_profile(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': '用户不存在!'}), 404
    
    profile = UserProfile.query.filter_by(user_id=user_id).first()
    
    return jsonify({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'wallet_address': user.wallet_address,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
        },
        'profile': {
            'bio': profile.bio if profile else '',
            'avatar_url': profile.avatar_url if profile else 'https://picsum.photos/200/200',
            'cover_url': profile.cover_url if profile else 'https://picsum.photos/800/300',
            'social_links': profile.social_links if profile else {}
        },
        'created_nfts': len(NFT.query.filter_by(creator_id=user_id).all()),
        'owned_nfts': len(NFT.query.filter_by(owner_id=user_id).all()),
        'total_sales': sum([tx.price for tx in Transaction.query.filter_by(seller_id=user_id).all()])
    }), 200

@app.route('/api/users/<int:user_id>/nfts', methods=['GET'])
def get_user_nfts(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': '用户不存在!'}), 404
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    type = request.args.get('type', 'owned')  # owned, created, for_sale
    
    if type == 'owned':
        nfts = NFT.query.filter_by(owner_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
    elif type == 'created':
        nfts = NFT.query.filter_by(creator_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
    elif type == 'for_sale':
        nfts = NFT.query.filter_by(owner_id=user_id, is_for_sale=True).paginate(page=page, per_page=per_page, error_out=False)
    else:
        return jsonify({'message': '无效的NFT类型!'}), 400
    
    return jsonify({
        'nfts': [{
            'id': nft.id,
            'token_id': nft.token_id,
            'name': nft.name,
            'description': nft.description,
            'image_url': nft.image_url,
            'creator': {
                'id': nft.creator_id,
                'username': User.query.get(nft.creator_id).username if User.query.get(nft.creator_id) else '未知'
            },
            'owner': {
                'id': nft.owner_id,
                'username': User.query.get(nft.owner_id).username if User.query.get(nft.owner_id) else '未知'
            },
            'price': nft.price,
            'royalty': nft.royalty,
            'created_at': nft.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'collection': nft.collection,
            'category': nft.category,
            'is_for_sale': nft.is_for_sale
        } for nft in nfts.items],
        'total': nfts.total,
        'pages': nfts.pages,
        'current_page': page
    }), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)    