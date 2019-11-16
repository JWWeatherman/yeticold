<template>
    <div class="container" style="margin-top: 3rem;">
      <h2>Yeti Bitcoin Storage</h2>
      <p>Yeti is currently pre-alpha. This means that not only is the code not well tested, but it isn't even functional yet. We would love help testing and code review and hope to have something usable and reasonably trustworthy within a few weeks.</p>
      <p>Yeti is a script that installs bitcoin core and then walks the user through setup of cold storage solution that has the following advantages:</p>
      <ul>
          <li>Private keys are never on any device with a channel to an Internet connected device except through QR codes. Solutions that use removable media or a USB cable to connect to a device connected to the internet could be used to send keys to an attacker. Because the only data that leaves device with private keys does so through QR codes all data can be easily verified and is very limited. We believe this is the smallest possible attack surface.</li>
          <li>A 3 of 7 multisig addresses is used for bitcoin storage. This allows up to 4 keys to be lost without losing bitcoin and requires 3 locations to be compromised by an attacker to lose funds. This prioritizes recovery and redundancy and we believe accidental loss is the most likely way for users to lose their bitcoin.</li>
          <li>HD Multisig is used so that you can send funds to 1,000 addresses, but recover all funds using only 3 seed phrases.</li>
          <li>Generic computing hardware is used. Hardware sold specifically for bitcoin storage requires trusting everyone from manufacturing to shipping to fail to realize the opportunity available to modify the hardware in order to steal bitcoin.</li>
          <li>Minimal software beyond bitcoin core. Bitcoin core is far and away the most trustworthy bitcoin software. Unfortunately it does not yet provide a user friendly interface for establishing a multisig address using an offline device or display and accept private keys in a human writable format. As bitcoin core adds these features we will reduce the Yeti code that provides these features now. Eventually we hope Yeti will be entirely unnecessary and only trusting bitcoin core will be required.</li>
          <li>Open source and easily audited. One of the reasons bitcoin core is trustworthy is that it is the most scrutinized software. This makes it the least likely to contain a critical security flaw that has not been identified and fixed. Yeti will never be as trustworthy, but by minimizing the amount of code and primarily using python scripts and console commands and a tiny amount of JavaScript the effort required to verify that Yeti is performing as expected is minimized.</li>
          <li>Usable for non-technical users. By following simple instructions users with moderate computer literacy can use Yeti. This is important because trusting someone to help you establish your cold storage solution introduces considerable risk.</li>
          <li>Private. Unlike many popular hardware and software wallets that transmit your IP address and bitcoin balance to third party servers, Yeti uses a bitcoin core full node. This means nothing is shared beyond what is required to create a bitcoin transaction. Yeti also uses Tor.</li>
          <li>Counterfeit prevention. The only way to be certain that your balance represents genuine bitcoin is to use a bitcoin full node - in fact that is the primary purpose of a bitcoin full node - to verify that the bitcoin balance is correct and full of only genuine bitcoins. Any solution that does not involve a full node requires you trust someone else to tell you if you have real bitcoin.</li>
          <li>The process can be completed by non technologists with minimal effort.</li>
          <li>Bitcoin private keys are stored on paper in multiple geographic locations with professionals that do not know they are storing bitcoin private keys.</li>
          <li>Private keys are written down using the NATO phonetic alphabet where every fifth word is a checksum to reduce the possibility that a private key will be unreadable when needed.</li>
          <li>Instructions for recovering the bitcoin are included with every copy of the private keys to reduce the likelihood of loss.</li>
      </ul>

      <p>While we believe Yeti provides the best balance of security, ease of use and cost when storing significant sums of bitcoin, it has the following disadvantages that might not be expected:</p>
      <ul>
          <li>Cost. You will need two computers and two external hard drives. If you need to purchase all of these items it should cost less than $500 USD, but this is not an insignificant expense.</li>
          <li>Time. To complete setup you will need to invest 4 hours spread over the course of 1-2 weeks. This time includes writing down security words, copying files and scanning QR codes.</li>
          <li>Privacy. While using bitcoin core over Tor does provide significant privacy advantages over many cold storage solutions using multisig is not very common and a 3 of 7 multisig is even less common. This means that someone could look at the blockchain and infer that the owner of the coins is probably using yeti for cold storage. This will eventually be fixed through changes to bitcoin and it is worth the security and recovery benefit to use multisig.</li>
      </ul>
      <a href="https://github.com/JWWeatherman/yetihosted" >The source code for the website that covers the first few steps can be found here:</a>
      <a href="https://github.com/JWWeatherman/yeticold" >The source code for the code that is downloaded to the online and offline laptops can be found here:</a>
      <input v-on:click="click" style="margin-bottom:50px;" class="btn btn-primary" type="submit" id="next" value="Next">
    </div>
</template>

<script>
export default {
  mounted () {
  },
  methods: {
    click () {
      this.$router.push({path: '/options'})
    }
  },
  computed: {
  },
  name: 'overview',
  data () {
    return {
      msg: 'Convert your passphrase key to a WIF private key'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
