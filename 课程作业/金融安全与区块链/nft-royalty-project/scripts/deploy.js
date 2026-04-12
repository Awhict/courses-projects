const { ethers } = require("hardhat");

async function main() {
  // 获取合约工厂
  const RoyaltyManager = await ethers.getContractFactory("RoyaltyManager");
  
  // 部署合约
  const royaltyManager = await RoyaltyManager.deploy();
  await royaltyManager.deployed();

  console.log("RoyaltyManager deployed to:", royaltyManager.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });