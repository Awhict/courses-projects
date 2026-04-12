const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("RoyaltyManager", function () {
  let royaltyManager;
  let owner, creator, buyer;

  beforeEach(async function () {
    // 获取测试账户
    [owner, creator, buyer] = await ethers.getSigners();

    // 部署合约
    const RoyaltyManager = await ethers.getContractFactory("RoyaltyManager");
    royaltyManager = await RoyaltyManager.deploy();
    await royaltyManager.deployed();
  });

  it("Should set and get token-level royalty info", async function () {
    // 允许NFT合约
    await royaltyManager.connect(owner).allowNFTContract(creator.address, true);
    
    // 设置版税（2%）
    await royaltyManager.connect(owner).setTokenRoyalty(
      creator.address, // NFT合约地址
      1,               // token ID
      creator.address, // 版税接收者
      200              // 2%版税 (200 * 0.01% = 2%)
    );

    // 查询版税信息
    const [recipient, royaltyAmount] = await royaltyManager.getRoyaltyInfo(
      creator.address,
      1,
      ethers.utils.parseEther("1") // 1 ETH售价
    );

    // 验证结果
    console.log("实际版税接收者:", recipient);
    console.log("实际版税金额:", ethers.utils.formatEther(royaltyAmount));
    console.log("预期版税金额:", ethers.utils.formatEther(ethers.utils.parseEther("0.02")));
    
    expect(recipient).to.equal(creator.address);
    expect(royaltyAmount).to.equal(ethers.utils.parseEther("0.02")); // 2% of 1 ETH
  });

  it("Should use contract-level royalty if token-level not set", async function () {
    // 允许NFT合约
    await royaltyManager.connect(owner).allowNFTContract(creator.address, true);
    
    // 设置合约级版税（3%）
    await royaltyManager.connect(owner).setContractRoyalty(
      creator.address,
      creator.address,
      300 // 3%版税
    );

    // 查询没有设置token级版税的NFT
    const [recipient, royaltyAmount] = await royaltyManager.getRoyaltyInfo(
      creator.address,
      1, // 未设置token级版税的token ID
      ethers.utils.parseEther("1")
    );

    // 验证结果
    expect(recipient).to.equal(creator.address);
    expect(royaltyAmount).to.equal(ethers.utils.parseEther("0.03")); // 3% of 1 ETH
  });

  it("Should prioritize token-level royalty over contract-level", async function () {
    // 允许NFT合约
    await royaltyManager.connect(owner).allowNFTContract(creator.address, true);
    
    // 设置合约级版税（3%）
    await royaltyManager.connect(owner).setContractRoyalty(
      creator.address,
      buyer.address, // 合约级版税接收者为buyer
      300
    );
    
    // 设置token级版税（2%）
    await royaltyManager.connect(owner).setTokenRoyalty(
      creator.address,
      1,
      creator.address, // token级版税接收者为creator
      200
    );

    // 查询token 1的版税
    const [recipient, royaltyAmount] = await royaltyManager.getRoyaltyInfo(
      creator.address,
      1,
      ethers.utils.parseEther("1")
    );

    // 验证结果（应使用token级设置）
    expect(recipient).to.equal(creator.address);
    expect(royaltyAmount).to.equal(ethers.utils.parseEther("0.02"));
  });

  it("Should revert if setting royalty for unallowed contract", async function () {
    // 尝试为未允许的合约设置版税
    await expect(
      royaltyManager.connect(owner).setTokenRoyalty(
        creator.address,
        1,
        creator.address,
        200
      )
    ).to.be.revertedWith("NFT contract not allowed");
  });

  it("Should revert if royalty rate exceeds 10%", async function () {
    // 允许NFT合约
    await royaltyManager.connect(owner).allowNFTContract(creator.address, true);
    
    // 尝试设置超过10%的版税
    await expect(
      royaltyManager.connect(owner).setTokenRoyalty(
        creator.address,
        1,
        creator.address,
        1001 // 超过10% (1000 = 10%)
      )
    ).to.be.revertedWith("Royalty rate cannot exceed 10%");
  });

  it("Should pay royalty correctly", async function () {
    // 允许NFT合约
    await royaltyManager.connect(owner).allowNFTContract(creator.address, true);
    
    // 设置版税（2%）
    await royaltyManager.connect(owner).setTokenRoyalty(
      creator.address,
      1,
      creator.address,
      200
    );

    // 记录创作者初始余额
    const initialCreatorBalance = await ethers.provider.getBalance(creator.address);
    
    // 支付版税（发送1 ETH，其中0.02 ETH作为版税）
    const tx = await royaltyManager.connect(buyer).payRoyalty(
      creator.address,
      1,
      ethers.utils.parseEther("1"),
      { value: ethers.utils.parseEther("1") }
    );
    
    // 等待交易确认
    await tx.wait();
    
    // 记录创作者最终余额
    const finalCreatorBalance = await ethers.provider.getBalance(creator.address);
    
    // 计算创作者收到的版税
    const royaltyReceived = finalCreatorBalance.sub(initialCreatorBalance);
    
    // 验证版税金额
    expect(royaltyReceived).to.equal(ethers.utils.parseEther("0.02"));
  });
});