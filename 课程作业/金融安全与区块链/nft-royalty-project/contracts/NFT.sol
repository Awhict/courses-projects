// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

/**
 * @title ArtBlockNFT
 * @dev 基于ERC721C标准的数字藏品合约
 */
contract ArtBlockNFT is ERC721, ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIdCounter;
    
    // 藏品版税信息
    struct RoyaltyInfo {
        address creator;
        uint96 royaltyPercentage; // 版税百分比，以0.01%为单位，例如500代表5%
    }
    
    // 存储每个token的版税信息
    mapping(uint256 => RoyaltyInfo) private _tokenRoyaltyInfo;
    
    constructor() ERC721("ArtBlockNFT", "ABNFT") {}
    
    /**
     * @dev 铸造新的NFT
     * @param to 接收NFT的地址
     * @param uri NFT的元数据URI
     * @param royaltyPercentage 版税百分比，以0.01%为单位，例如500代表5%
     */
    function mint(address to, string memory uri, uint96 royaltyPercentage) public onlyOwner returns (uint256) {
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
        
        // 设置版税信息
        _tokenRoyaltyInfo[tokenId] = RoyaltyInfo({
            creator: to,
            royaltyPercentage: royaltyPercentage
        });
        
        return tokenId;
    }
    
    /**
     * @dev 获取NFT的版税信息
     * @param tokenId NFT的token ID
     * @param salePrice 销售价格
     * @return receiver 版税接收地址
     * @return royaltyAmount 版税金额
     */
    function royaltyInfo(uint256 tokenId, uint256 salePrice) external view returns (address receiver, uint256 royaltyAmount) {
        RoyaltyInfo memory info = _tokenRoyaltyInfo[tokenId];
        receiver = info.creator;
        royaltyAmount = (salePrice * info.royaltyPercentage) / 10000;
    }
    
    /**
     * @dev 批量获取NFT的版税信息
     * @param tokenIds NFT的token ID数组
     * @param salePrices 销售价格数组
     * @return receivers 版税接收地址数组
     * @return royaltyAmounts 版税金额数组
     */
    function royaltyInfoBatch(uint256[] memory tokenIds, uint256[] memory salePrices) external view returns (address[] memory receivers, uint256[] memory royaltyAmounts) {
        require(tokenIds.length == salePrices.length, "Input arrays must have the same length");
        
        receivers = new address[](tokenIds.length);
        royaltyAmounts = new uint256[](tokenIds.length);
        
        for (uint256 i = 0; i < tokenIds.length; i++) {
            RoyaltyInfo memory info = _tokenRoyaltyInfo[tokenIds[i]];
            receivers[i] = info.creator;
            royaltyAmounts[i] = (salePrices[i] * info.royaltyPercentage) / 10000;
        }
    }
    
    /**
     * @dev 获取NFT的创造者
     * @param tokenId NFT的token ID
     * @return creator NFT的创造者地址
     */
    function getCreator(uint256 tokenId) external view returns (address creator) {
        return _tokenRoyaltyInfo[tokenId].creator;
    }
    
    /**
     * @dev 获取NFT的版税百分比
     * @param tokenId NFT的token ID
     * @return percentage 版税百分比，以0.01%为单位，例如500代表5%
     */
    function getRoyaltyPercentage(uint256 tokenId) external view returns (uint96 percentage) {
        return _tokenRoyaltyInfo[tokenId].royaltyPercentage;
    }
    
    /**
     * @dev 更新NFT的版税信息
     * @param tokenId NFT的token ID
     * @param newRoyaltyPercentage 新的版税百分比，以0.01%为单位，例如500代表5%
     */
    function updateRoyaltyInfo(uint256 tokenId, uint96 newRoyaltyPercentage) external {
        require(_isApprovedOrOwner(_msgSender(), tokenId), "Caller is not owner nor approved");
        _tokenRoyaltyInfo[tokenId].royaltyPercentage = newRoyaltyPercentage;
    }
    
    // 修复supportsInterface函数的继承冲突
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
    
    // The following functions are overrides required by Solidity.
    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }
    
    function tokenURI(uint256 tokenId) public view override(ERC721, ERC721URIStorage) returns (string memory) {
        return super.tokenURI(tokenId);
    }
}