// V5/frontend/script.js
document.addEventListener('DOMContentLoaded', async () => {
    // 检查是否安装了 MetaMask
    if (typeof window.ethereum === 'undefined') {
        alert('请安装 MetaMask 钱包以使用此应用程序。');
        return;
    }

    const web3 = new Web3(window.ethereum);

    // 请求用户授权连接 MetaMask
    try {
        await window.ethereum.request({ method: 'eth_requestAccounts' });
        const accounts = await web3.eth.getAccounts();
        console.log('当前账户:', accounts[0]);
    } catch (error) {
        console.error('用户拒绝授权或发生错误:', error);
    }

    // 处理连接钱包按钮点击事件
    const walletConnectBtn = document.getElementById('walletConnectBtn');
    const mobileWalletConnectBtn = document.getElementById('mobileWalletConnectBtn');

    const connectWallet = async () => {
        try {
            await window.ethereum.request({ method: 'eth_requestAccounts' });
            const accounts = await web3.eth.getAccounts();
            console.log('已连接账户:', accounts[0]);
            // 可以在这里更新 UI 显示已连接的账户信息
        } catch (error) {
            console.error('连接钱包时发生错误:', error);
        }
    };

    walletConnectBtn.addEventListener('click', connectWallet);
    mobileWalletConnectBtn.addEventListener('click', connectWallet);
});