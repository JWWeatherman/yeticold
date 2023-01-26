<template>
    <div class="container" style="margin-top: 3rem;">
      <h2>YetiCold.com Bitcoin Storage</h2>
        <h3>Setup Instructions</h3>
        <p>https://yeticold.com</p>
        <p>Mirror https://jwweatherman.github.io</p>
      <p>Yeti is the safest option for bitcoin cold storage, however bitcoin is still in the "early adopter" phase. This means it is not as easy or fun as it will become eventually so you'll need to be patient and humble if you want to earn the rewards associated with being an early user of new technology.</p>
      <p>Yeti is a script that installs bitcoin core and then walks the user through setup of cold storage solution that has the following advantages:</p>
      <ul>
          <li>Yeti prioritizes safety over ease of use. For example hardware wallets should never be used with a daily use laptop, but because this requires about an hour of work it is not part of the instructions. Yeti takes the opposite approach and requires users do what is needed for safe and secure bitcoin storage even when this requires more time and effort - the first task in the Yeti instructions is to setup trustworthy laptops.</li>
          <li>Private keys are never on any device with a channel to an Internet connected device except through USB drives. Although we would prefer to use QR codes bitcoin core does not support offline signing via QR codes and the additional attack surface we would need to introduce to support this might outweigh the benefits. The purpose of an "air gap" is to limit the amount of data that can be moved, limit the times data can be moved, and make it easy to verify the data is accurate "out of band" before sending. USB drives are inferior to QR codes in all of these areas, but the risk that a QR code library has a security flaw must be weighed against these advantages. </li>
          <li>A 3 of 7 multisig addresses is used for bitcoin storage. This allows up to 4 keys to be lost without losing bitcoin and requires 3 locations to be compromised by an attacker to lose funds. This prioritizes recovery and redundancy and we believe accidental loss is the most likely way for users to lose their bitcoin.</li>
          <li>HD Multisig is used so that you can send funds to 1,000 addresses, but recover all funds using only 3 seed phrases.</li>
          <li>Generic computing hardware is used. Hardware sold specifically for bitcoin storage requires trusting everyone from manufacturing to shipping to fail to realize the opportunity available to modify the hardware in order to steal bitcoin.</li>
          <li>Minimal software beyond bitcoin core. Bitcoin core is far and away the most trustworthy bitcoin software. Unfortunately it does not yet provide a user friendly interface for establishing a multisig address or display and accept private keys in a human writable format. As bitcoin core adds these features we will reduce the Yeti code that provides these features now. Eventually we hope Yeti will be entirely unnecessary and only trusting bitcoin core will be required.</li>
          <li>Open source and easily audited. One of the reasons bitcoin core is trustworthy is that it is the most scrutinized software. This makes it the least likely to contain a critical security flaw that has not been identified and fixed. Yeti will never be as trustworthy, but by minimizing the amount of code and primarily using python scripts and console commands and a tiny amount of JavaScript the effort required to verify that Yeti is performing as expected is minimized.</li>
          <li>Usable for non-technical users. By following simple instructions users with moderate computer literacy can use Yeti. This is important because trusting someone to help you establish your cold storage solution introduces considerable risk.</li>
          <li>Private keys are stored in non-descript packaging and stored with people that do not know they contain private keys.</li>
          <li>Private. Unlike many popular hardware and software wallets that transmit your IP address (home address) and bitcoin balance to third party servers, Yeti uses a bitcoin core full node. This means nothing is shared beyond what is required to create a bitcoin transaction. Yeti also uses Tor.</li>
          <li>Counterfeit prevention. The only way to be certain that your balance represents genuine bitcoin is to use a bitcoin full node - in fact that is the primary purpose of a bitcoin full node - to verify that the bitcoin balance is correct and full of only genuine bitcoins. Any solution that does not involve a full node requires you trust someone else to tell you if you have real bitcoin.</li>
<Li>Minimal hardware. You only need access to two cheap computers. If you don't own a laptop you can buy one from a big box store and return it after setup is completed.</li>
          <li>The process can be completed by non technologists with minimal effort.</li>
          <li>Bitcoin private keys are stored on paper in multiple geographic locations with professionals that do not know they are storing bitcoin private keys.</li>
          <li>Private keys are written down using the NATO phonetic alphabet where every fifth word is a checksum to reduce the possibility that a private key will be unreadable when needed.</li>
          <li>Instructions for recovering the bitcoin are included with every copy of the private keys to reduce the likelihood of loss.</li>
      </ul>
      <p>While we believe Yeti provides the best balance of security, ease of use and cost when storing significant sums of bitcoin, it has the following disadvantages that might not be expected:</p>
      <ul>
          <li>Time. To complete setup you will need to invest 2 hours spread over the course of a couple days. This time includes writing down security words, copying files and scanning QR codes.</li>
          <li>Privacy. While using bitcoin core over Tor does provide significant privacy advantages over many cold storage solutions, using multisig is not very common and a 3 of 7 multisig is even less common. This means that someone could look at the blockchain and infer that the owner of the coins is probably using Yeti for cold storage. This will eventually be fixed through changes to bitcoin and it is worth the security and recovery benefit to use multisig and the type of multisig you are using is only exposed to the network when you spend from Yeti (not when you deposit funds).</li>
        </ul>
        <p>For support join our slack channel https://join.slack.com/t/yeticold/shared_invite/zt-1lwka5184-NSDwVpxl7mGHykqfqblCzg</p>
        <p>For more reading checkout our FAQ https://github.com/JWWeatherman/yeticold/blob/master/FAQ.md</p>
    </div>
</template>

