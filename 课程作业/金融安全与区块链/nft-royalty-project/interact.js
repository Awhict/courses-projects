const { ethers } = require("ethers");

async function interactWithContract() {
  // 连接到本地Hardhat网络
  const provider = new ethers.providers.JsonRpcProvider("http://localhost:8545");
  
  // 获取第一个测试账户（部署者）
  const signer = provider.getSigner(0);
  
  // 合约ABI（从artifacts目录获取）
  const abi = [
    // 复制RoyaltyManager合约的ABI
    // 可以从artifacts/contracts/RoyaltyManager.sol/RoyaltyManager.json获取
  ];
  
  // 合约地址
  const contractAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3";
  
  // 创建合约实例
  const royaltyManager = new ethers.Contract(contractAddress, abi, signer);
  
  // 调用合约函数
  const tx = await royaltyManager.allowNFTContract("0xYourNFTContractAddress", true);
  await tx.wait();
  
  console.log("NFT合约已被允许使用版税管理");
}

interactWithContract().catch(console.error);