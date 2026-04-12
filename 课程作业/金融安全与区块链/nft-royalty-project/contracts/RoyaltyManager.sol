// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title RoyaltyManager
 * @dev NFT市场版税管理合约，处理版税的设置、查询和分配
 */
contract RoyaltyManager is Ownable, ReentrancyGuard {
    // 版税信息结构
    struct RoyaltyInfo {
        address recipient;     // 版税接收者
        uint96 royaltyRate;    // 版税率，以0.01%为单位，例如200代表2%
    }
    
    // NFT合约地址 => token ID => 版税信息
    mapping(address => mapping(uint256 => RoyaltyInfo)) private tokenRoyalties;
    
    // NFT合约地址 => 合约级版税信息
    mapping(address => RoyaltyInfo) private contractRoyalties;
    
    // 允许的NFT合约列表
    mapping(address => bool) public allowedNFTContracts;
    
    // 事件
    event RoyaltySet(address indexed nftContract, uint256 indexed tokenId, address recipient, uint96 royaltyRate);
    event ContractRoyaltySet(address indexed nftContract, address recipient, uint96 royaltyRate);
    event NFTContractAllowed(address indexed nftContract, bool allowed);
    event RoyaltyPaid(address indexed nftContract, uint256 indexed tokenId, address recipient, uint256 amount);
    
    /**
     * @dev 设置特定NFT的版税信息
     * @param nftContract NFT合约地址
     * @param tokenId NFT的token ID
     * @param recipient 版税接收者地址
     * @param royaltyRate 版税率，以0.01%为单位，例如200代表2%
     */
    function setTokenRoyalty(
        address nftContract,
        uint256 tokenId,
        address recipient,
        uint96 royaltyRate
    ) external onlyOwner {
        require(allowedNFTContracts[nftContract], "NFT contract not allowed");
        require(royaltyRate <= 1000, "Royalty rate cannot exceed 10%");
        require(recipient != address(0), "Recipient address cannot be zero");
        
        tokenRoyalties[nftContract][tokenId] = RoyaltyInfo({
            recipient: recipient,
            royaltyRate: royaltyRate
        });
        
        emit RoyaltySet(nftContract, tokenId, recipient, royaltyRate);
    }
    
    /**
     * @dev 设置NFT合约级别的版税信息
     * @param nftContract NFT合约地址
     * @param recipient 版税接收者地址
     * @param royaltyRate 版税率，以0.01%为单位，例如200代表2%
     */
    function setContractRoyalty(
        address nftContract,
        address recipient,
        uint96 royaltyRate
    ) external onlyOwner {
        require(allowedNFTContracts[nftContract], "NFT contract not allowed");
        require(royaltyRate <= 1000, "Royalty rate cannot exceed 10%");
        require(recipient != address(0), "Recipient address cannot be zero");
        
        contractRoyalties[nftContract] = RoyaltyInfo({
            recipient: recipient,
            royaltyRate: royaltyRate
        });
        
        emit ContractRoyaltySet(nftContract, recipient, royaltyRate);
    }
    
    /**
     * @dev 允许或禁止NFT合约使用版税管理
     * @param nftContract NFT合约地址
     * @param allowed 是否允许
     */
    function allowNFTContract(address nftContract, bool allowed) external onlyOwner {
        allowedNFTContracts[nftContract] = allowed;
        emit NFTContractAllowed(nftContract, allowed);
    }
    
    /**
     * @dev 获取特定NFT的版税信息
     * @param nftContract NFT合约地址
     * @param tokenId NFT的token ID
     * @param salePrice 销售价格
     * @return recipient 版税接收者地址
     * @return royaltyAmount 版税金额
     */
    function getRoyaltyInfo(
        address nftContract,
        uint256 tokenId,
        uint256 salePrice
    ) public view returns (address recipient, uint256 royaltyAmount) {
        RoyaltyInfo memory tokenRoyalty = tokenRoyalties[nftContract][tokenId];
        
        // 如果特定NFT有版税设置，使用该设置
        if (tokenRoyalty.recipient != address(0)) {
            royaltyAmount = (salePrice * tokenRoyalty.royaltyRate) / 10000;
            return (tokenRoyalty.recipient, royaltyAmount);
        }
        
        // 否则使用合约级版税设置
        RoyaltyInfo memory contractRoyalty = contractRoyalties[nftContract];
        if (contractRoyalty.recipient != address(0)) {
            royaltyAmount = (salePrice * contractRoyalty.royaltyRate) / 10000;
            return (contractRoyalty.recipient, royaltyAmount);
        }
        
        // 如果都没有设置，返回0
        return (address(0), 0);
    }
    
    /**
     * @dev 支付版税
     * @param nftContract NFT合约地址
     * @param tokenId NFT的token ID
     * @param salePrice 销售价格
     * @return success 是否成功支付版税
     */
    function payRoyalty(
        address nftContract,
        uint256 tokenId,
        uint256 salePrice
    ) external payable nonReentrant returns (bool success) {
        (address recipient, uint256 royaltyAmount) = getRoyaltyInfo(nftContract, tokenId, salePrice);
        
        if (recipient == address(0) || royaltyAmount == 0) {
            return false;
        }
        
        require(msg.value >= royaltyAmount, "Insufficient funds sent for royalty");
        
        // 支付版税
        payable(recipient).transfer(royaltyAmount);
        
        // 如果有退款，退还多余的ETH
        if (msg.value > royaltyAmount) {
            payable(msg.sender).transfer(msg.value - royaltyAmount);
        }
        
        emit RoyaltyPaid(nftContract, tokenId, recipient, royaltyAmount);
        return true;
    }
    
    /**
     * @dev 提取合约中的ETH余额（紧急情况使用）
     */
    function emergencyWithdraw() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
    
    /**
     * @dev 合约接收ETH的fallback函数
     */
    receive() external payable {}
}    