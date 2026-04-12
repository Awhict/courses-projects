// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "./NFT.sol";

/**
 * @title ArtBlockNFTMarketplace
 * @dev 数字藏品交易市场合约
 */
contract ArtBlockNFTMarketplace is Ownable, ReentrancyGuard {
    // 平台费用比例，以0.01%为单位，例如200代表2%
    uint96 public platformFeePercentage = 200;
    
    // 争议期时长（秒）
    uint256 public disputePeriod = 72 hours;
    
    // 平台收益地址
    address public platformWallet;
    
    // 稳定币地址（用于平台收益自动兑换）
    address public stablecoinAddress;
    
    // 交易状态
    enum SaleStatus { Active, Completed, Canceled, Dispute }
    
    // 交易信息
    struct Sale {
        uint256 tokenId;
        address nftContract;
        address seller;
        address buyer;
        uint256 price;
        SaleStatus status;
        uint256 createdAt;
        uint256 updatedAt;
        uint256 disputeEndTime;
    }
    
    // 存储所有交易
    mapping(uint256 => Sale) public sales;
    uint256 public saleCount;
    
    // 事件
    event ItemListed(uint256 indexed saleId, address indexed nftContract, uint256 indexed tokenId, address seller, uint256 price);
    event ItemSold(uint256 indexed saleId, address indexed nftContract, uint256 indexed tokenId, address seller, address buyer, uint256 price);
    event ItemCanceled(uint256 indexed saleId, address indexed nftContract, uint256 indexed tokenId, address seller);
    event DisputeStarted(uint256 indexed saleId, address indexed nftContract, uint256 indexed tokenId, address buyer);
    event DisputeResolved(uint256 indexed saleId, address indexed nftContract, uint256 indexed tokenId, address winner);
    
    constructor(address _platformWallet, address _stablecoinAddress) {
        platformWallet = _platformWallet;
        stablecoinAddress = _stablecoinAddress;
    }
    
    /**
     * @dev 列出NFT供出售
     * @param nftContract NFT合约地址
     * @param tokenId NFT的token ID
     * @param price 出售价格（Wei）
     */
    function listItem(address nftContract, uint256 tokenId, uint256 price) external nonReentrant {
        require(price > 0, "Price must be greater than 0");
        
        // 检查调用者是否是NFT所有者
        IERC721 nft = IERC721(nftContract);
        require(nft.ownerOf(tokenId) == msg.sender, "Not the owner of this NFT");
        
        // 检查NFT是否已被批准给市场合约
        require(nft.getApproved(tokenId) == address(this) || nft.isApprovedForAll(msg.sender, address(this)), "Marketplace is not approved to transfer this NFT");
        
        // 创建新交易
        saleCount++;
        sales[saleCount] = Sale({
            tokenId: tokenId,
            nftContract: nftContract,
            seller: msg.sender,
            buyer: address(0),
            price: price,
            status: SaleStatus.Active,
            createdAt: block.timestamp,
            updatedAt: block.timestamp,
            disputeEndTime: 0
        });
        
        emit ItemListed(saleCount, nftContract, tokenId, msg.sender, price);
    }
    
    /**
     * @dev 购买NFT
     * @param saleId 交易ID
     */
    function buyItem(uint256 saleId) external payable nonReentrant {
        Sale storage sale = sales[saleId];
        
        require(sale.status == SaleStatus.Active, "Item is not for sale");
        require(msg.value >= sale.price, "Insufficient funds sent");
        
        // 转移NFT到买家
        IERC721(sale.nftContract).safeTransferFrom(sale.seller, msg.sender, sale.tokenId);
        
        // 计算平台费用
        uint256 platformFee = (sale.price * platformFeePercentage) / 10000;
        
        // 计算版税
        uint256 royaltyAmount = 0;
        address royaltyReceiver = address(0);
        
        // 尝试获取版税信息
        try ArtBlockNFT(sale.nftContract).royaltyInfo(sale.tokenId, sale.price) returns (address receiver, uint256 amount) {
            royaltyReceiver = receiver;
            royaltyAmount = amount;
        } catch {
            // 如果合约不支持版税，版税为0
        }
        
        // 计算卖家实际收入
        uint256 sellerRevenue = sale.price - platformFee - royaltyAmount;
        
        // 支付版税
        if (royaltyAmount > 0 && royaltyReceiver != address(0)) {
            payable(royaltyReceiver).transfer(royaltyAmount);
        }
        
        // 支付卖家
        payable(sale.seller).transfer(sellerRevenue);
        
        // 支付平台费用
        payable(platformWallet).transfer(platformFee);
        
        // 更新交易状态
        sale.buyer = msg.sender;
        sale.status = SaleStatus.Completed;
        sale.updatedAt = block.timestamp;
        
        // 如果有退款，退还多余的ETH
        if (msg.value > sale.price) {
            payable(msg.sender).transfer(msg.value - sale.price);
        }
        
        emit ItemSold(saleId, sale.nftContract, sale.tokenId, sale.seller, msg.sender, sale.price);
    }
    
    /**
     * @dev 取消NFT出售
     * @param saleId 交易ID
     */
    function cancelSale(uint256 saleId) external nonReentrant {
        Sale storage sale = sales[saleId];
        
        require(sale.status == SaleStatus.Active, "Item is not active");
        require(msg.sender == sale.seller, "Only seller can cancel the sale");
        
        // 更新交易状态
        sale.status = SaleStatus.Canceled;
        sale.updatedAt = block.timestamp;
        
        emit ItemCanceled(saleId, sale.nftContract, sale.tokenId, msg.sender);
    }
    
    /**
     * @dev 发起交易争议
     * @param saleId 交易ID
     */
    function startDispute(uint256 saleId) external nonReentrant {
        Sale storage sale = sales[saleId];
        
        require(sale.status == SaleStatus.Completed, "Item must be completed to start dispute");
        require(msg.sender == sale.buyer, "Only buyer can start a dispute");
        require(block.timestamp < sale.updatedAt + disputePeriod, "Dispute period has expired");
        
        // 更新交易状态
        sale.status = SaleStatus.Dispute;
        sale.disputeEndTime = block.timestamp + disputePeriod;
        sale.updatedAt = block.timestamp;
        
        emit DisputeStarted(saleId, sale.nftContract, sale.tokenId, msg.sender);
    }
    
    /**
     * @dev 解决交易争议
     * @param saleId 交易ID
     * @param refundBuyer 是否退款给买家
     */
    function resolveDispute(uint256 saleId, bool refundBuyer) external nonReentrant onlyOwner {
        Sale storage sale = sales[saleId];
        
        require(sale.status == SaleStatus.Dispute, "No active dispute for this item");
        
        if (refundBuyer) {
            // 退还买家资金（简化实现，实际应用中可能需要更复杂的逻辑）
            payable(sale.buyer).transfer(sale.price);
            
            // 转移NFT回卖家
            IERC721(sale.nftContract).safeTransferFrom(sale.buyer, sale.seller, sale.tokenId);
            
            emit DisputeResolved(saleId, sale.nftContract, sale.tokenId, sale.buyer);
        } else {
            emit DisputeResolved(saleId, sale.nftContract, sale.tokenId, sale.seller);
        }
        
        // 更新交易状态
        sale.status = SaleStatus.Completed;
        sale.updatedAt = block.timestamp;
    }
    
    /**
     * @dev 获取指定NFT的所有交易记录
     * @param nftContract NFT合约地址
     * @param tokenId NFT的token ID
     * @return 交易记录数组
     */
    function getSalesForNFT(address nftContract, uint256 tokenId) external view returns (Sale[] memory) {
        uint256 count = 0;
        
        // 计算符合条件的交易数量
        for (uint256 i = 1; i <= saleCount; i++) {
            if (sales[i].nftContract == nftContract && sales[i].tokenId == tokenId) {
                count++;
            }
        }
        
        // 创建结果数组
        Sale[] memory result = new Sale[](count);
        uint256 index = 0;
        
        // 填充结果数组
        for (uint256 i = 1; i <= saleCount; i++) {
            if (sales[i].nftContract == nftContract && sales[i].tokenId == tokenId) {
                result[index] = sales[i];
                index++;
            }
        }
        
        return result;
    }
    
    /**
     * @dev 获取用户的所有购买记录
     * @param user 用户地址
     * @return 交易记录数组
     */
    function getPurchasesByUser(address user) external view returns (Sale[] memory) {
        uint256 count = 0;
        
        // 计算符合条件的交易数量
        for (uint256 i = 1; i <= saleCount; i++) {
            if (sales[i].buyer == user && sales[i].status == SaleStatus.Completed) {
                count++;
            }
        }
        
        // 创建结果数组
        Sale[] memory result = new Sale[](count);
        uint256 index = 0;
        
        // 填充结果数组
        for (uint256 i = 1; i <= saleCount; i++) {
            if (sales[i].buyer == user && sales[i].status == SaleStatus.Completed) {
                result[index] = sales[i];
                index++;
            }
        }
        
        return result;
    }
    
    /**
     * @dev 获取用户的所有出售记录
     * @param user 用户地址
     * @return 交易记录数组
     */
    function getSalesByUser(address user) external view returns (Sale[] memory) {
        uint256 count = 0;
        
        // 计算符合条件的交易数量
        for (uint256 i = 1; i <= saleCount; i++) {
            if (sales[i].seller == user && (sales[i].status == SaleStatus.Active || sales[i].status == SaleStatus.Completed)) {
                count++;
            }
        }
        
        // 创建结果数组
        Sale[] memory result = new Sale[](count);
        uint256 index = 0;
        
        // 填充结果数组
        for (uint256 i = 1; i <= saleCount; i++) {
            if (sales[i].seller == user && (sales[i].status == SaleStatus.Active || sales[i].status == SaleStatus.Completed)) {
                result[index] = sales[i];
                index++;
            }
        }
        
        return result;
    }
    
    /**
     * @dev 设置平台费用比例
     * @param newFeePercentage 新的平台费用比例，以0.01%为单位，例如200代表2%
     */
    function setPlatformFeePercentage(uint96 newFeePercentage) external onlyOwner {
        require(newFeePercentage <= 1000, "Fee percentage cannot exceed 10%");
        platformFeePercentage = newFeePercentage;
    }
    
    /**
     * @dev 设置争议期时长
     * @param newDisputePeriod 新的争议期时长（秒）
     */
    function setDisputePeriod(uint256 newDisputePeriod) external onlyOwner {
        disputePeriod = newDisputePeriod;
    }
    
    /**
     * @dev 设置平台收益地址
     * @param newPlatformWallet 新的平台收益地址
     */
    function setPlatformWallet(address newPlatformWallet) external onlyOwner {
        platformWallet = newPlatformWallet;
    }
    
    /**
     * @dev 设置稳定币地址
     * @param newStablecoinAddress 新的稳定币地址
     */
    function setStablecoinAddress(address newStablecoinAddress) external onlyOwner {
        stablecoinAddress = newStablecoinAddress;
    }
    
    /**
     * @dev 将平台收益兑换为稳定币（简化实现）
     * @param amount 要兑换的金额（Wei）
     */
    function convertPlatformRevenueToStablecoin(uint256 amount) external onlyOwner {
        // 这里应该实现将ETH兑换为稳定币的逻辑
        // 简化实现，实际应用中可能需要集成去中心化交易所
        emit PlatformRevenueConverted(amount, stablecoinAddress);
    }
    
    event PlatformRevenueConverted(uint256 amount, address stablecoin);
}    