### How can I get an overview of Yeti?
The first step on each level of Yeti provides a link to a complete video walk through. Grab some popcorn and enjoy.

Level 1
https://yeticold.com/Hot/step1

Level 2
https://yeticold.com/Warm/step1

Level 3
https://yeticold.com/Cold/step1

### Should I read this FAQ if I am a normal user?
Probably not. Yeti was designed so that you can simply start at yeticold.com and follow simple instructions to end up with a bitcoin wallet that is appropriate for the amount of bitcoin you are storing. If you get stuck on a step you should watch the videos linked above or reach out on slack:

https://join.slack.com/t/yeticold/shared_invite/zt-hisfxrra-BZzrYCDnqFv6whxVn~6FQQ

### How much knowledge of Linux is required?
None. Installing Ubuntu is the only challenging task and it is no more difficult than installing Windows or Mac OS. Even if you have never installed an OS before it is not difficult and you can get support from our slack channel at:

https://join.slack.com/t/yeticold/shared_invite/zt-hisfxrra-BZzrYCDnqFv6whxVn~6FQQ

You can also hire a local computer shop to install Ubuntu for you for about $30 and as long as they don't suspect you will use this laptop for bitcoin it is a reasonably safe option.

### How much time does it take to set up the first time?
The most time consuming part of yeti is waiting for bitcoin core to sync with the network. With an SSD drive this can be done overnight, but if you have an HDD (old style) drive it could take up to a week.

For the part where you are actually doing something it takes less than an hour.

### Why should I trust Yeti with my life savings?
You should not trust us, but you should trust the incentives of open source software development. Projects like bitcoin core are trustworthy because they are open source and very popular. Anyone can read the code and find a flaw that could allow you to lose your bitcoin. But that is not enough because many open source project are not ignored by all but a very small number of people that do not have a good reputation. So the project must also be very popular. Bitcoin core is the most and most trusted bitcoin software on the planet. This means that any developer that is skilled and interested in bitcoin has probably reviewed bitcoin core to understand how bitcoin works and to find opportunities to improve it. If a developer or security researcher found a major flaw in bitcoin core they would be instantly domain famous and receive lucrative job offers. Finding a major flaw is a career making opportunity. 

This is also the case with Ubuntu and other <b>popular</b> open source software. However Yeti is not that popular yet - therefore it is not nearly as trustworthy. In fact all bitcoin software outside of bitcoin core is much less trustworthy because it is much less popular. Yeti mitigates this a few ways:

- Yeti does not do anything security critical. All important tasks, like generating random numbers, is handled by bitcoin core.
- Yeti is a setup script. Once you wallet you do not use yeti software to send or receive transactions - yeti simply helps you setup bitcoin core using best practices.
- Yeti uses Python. This is one of the easiest languages to learn and read. Even a non-developer can spend a few hours reviewing the Yeti setup script to verify that it is not doing anything dishonest or dangerous. This also makes it very cheap to hire a developer to review the Yeti code. The best way to do this is to begin the setup steps until you have downloaded the yeti code to your offline laptop found in the "yeticold" folder in your home directory. Then using a false name sign up for a service like upwork.com or fiverr.com or ever Twitter and hire a Python developer. Give them the "yeticold" folder and the website and ask them to review the code in the folder to make sure it is trustworthy. Be sure to tell them that bitcoin core is out of scope and should be assumed trustworthy. Many Yeti users have told us that they have done this for less than $100 USD (often closer to $10). 
- Yeti is small and optimized for reading. The Yeti code is only a few hundred lines (probably shorter than this FAQ). It could be much smaller, but our priority is in making it as easy as possible to read.
- Yeti is also a temporary project. When Yeti was first released it was the only way to use bitcoin core as an offline signing device. A year later the bitcoin core team added offline signing and the Yeti team was able to delete about 1/3 of the project code. Yeti contributors are currently offering bounties to add QR codes and multisig wallet creation in bitcoin core. That will allow us to delete about 1/3 more of our code. Eventually Yeti will be nothing more than a document and help
  video to walk you through bitcoin core setup.
- Yeti offers credible bug bounties. Unlike most projects including Casa, Cold Card and others Yeti has never failed to reward security researchers for finding a flaw that could allow attackers to steal funds. Yeti currently offers a 1 BTC bug bounty and has even offered all hardware wallets a 1 BTC bet (on multiple occasions) that they will have a new security critical bug before Yeti has it's first. No hardware wallet company has accepted our bet.
- Yeti can be used without our "code." @BenWestgate_ on twitter is a Yeti contributor that has written a combination of shell scripts and direct RPC commands to bitcoin core that can be used by anyone that finds this easier to verify. 

### Do I need to download the whole blockchain if I already have a node?
No. If you have a .bitcoin folder that is completely trustworthy you can copy it into the home directory before you begin. However if you generated the .bitcoin folder on a computer that has malware it is possible that you will be introducing that to your trustworthy laptop by copying over the .bitcoin folder so this is only recommended for advanced users. Once you setup Yeti you will have a trustworthy .bitcoin folder on your internet connected laptop so making a backup on an external
hard drive is a reasonable thing to do, but you need to be careful to delete any wallet.dat iles so this is also only recommened for advanced users. You certainly do not want to use a .bitcoin folder from someone else unless is it only for testing with tiny amounts.

### Does it make sense to get a faster laptop to speed up the process?
Probably not as you will only work with yeti a couple times a year so you won't get a ton of use out of faster hardware. However, an SSD drive is about $50 and makes syncing much faster so if you are a bitcoin enthusiast and you like to test and experiment with bitcoin core it is worth doing.

### What are the minimum specs for the laptops?
A laptop(s) that can run Ubuntu and Bitcoin Core is required. At the time of this writing almost any laptop will work but if your laptop has an SSD type hard drive some steps will take a few hours instead of a few days. Laptops without SSD type drives cost about $150 USD and laptops with SSD drives cost about $200 USD.

### Why do I need a printer?
You only need a printer for Level 3 and it is used to print out recovery instructions. The printer will not be used to print your seed words.

### What kind of CDs should I buy?
You don't need to buy any special type of CDs. For Level 1 and Level 2 you will have multiple copies of any important data stored on CDs and Level 3 you also have a paper backup in case your CDs are lost or damaged. All CDs are much better storage devices than any USB or hardware wallet storage devices because a laser is used to 
burn a thin piece of plastic to store a 1 or 0 instead of a tiny amount of electrical charge. This is much more reliable for long term storage.

### When using Level 3 it requires two laptops, do the laptops need to be the same?
No. Any laptops that can run Ubuntu and Bitcoin core will work great.

### What USB sticks are good to get?
Any cheap USB sticks will work fine. 

### Should I try to get a laptop without wifi?
No. Yeti disables your network connections before generating your seed words. It couldn't hurt to have a laptop without wifi or only use your Ethernet port for added assurance, but it's probably not worth the hassle.

### How can I make sure my seed phrases are safe?
When you follow the instructions in Yeti you will store your seed words in places like safety deposit boxes and home safes. For Level 2 and Level 3 an attacker would need to gain access to 3 of those locations so securing your seed words is much easier. 

### How is this better than a hardware wallet?
Hardware wallets can be very easy to use because people believe that they are safe even when they plug them into insecure devices like a daily driver laptop. This is false, but it does create an easy user experience that is fine for smaller amounts. This also means it is very easy to regularly spend from these devices. However for smaller amounts it is cheaper, safer and easier to use a single purpose phone using bluewallet.io than to use a hardware wallet so there is really no circumstance where a hardware wallet is appropriate.

To learn more about why hardware wallets are always the wrong choice see Robert Spigler's comprehensive review of hardware wallets:
https://robertspigler.wixsite.com/blog/in-defense-of-my-attack-on-hardware

And Greg Maxwell's criticism of hardware wallets for non-technical users (He specifically does not like them for non-technical users):
https://old.reddit.com/r/Bitcoin/comments/jp2fp3/opinion_regarding_security/gbbzqu7/

### How is using a laptop better than a hardware wallet?
Generic computing hardware is used. Hardware sold specifically for bitcoin storage requires trusting everyone from manufacturing to shipping to fail to realize the opportunity available to modify the hardware in order to steal bitcoin.

When you use a hardware wallet you are trusting the small team of people that write and review the code and everyone that has handled the hardware wallet before you got it. With yeti all important security functions are handled by bitcoin core and it has the best developers and the largest number of people checking for errors. 

You are also using Ubuntu and a generic laptop, but this is more secure as Ubuntu is reviewed by hundreds of developers for security issues and generic hardware makes "supply chain attacks" much more expensive.

### What's a good strategy for storing the seeds?
Always store your seeds with people and locations that do not know they are storing bitcoin seeds. For example your lawyer should believe he is storing "just another important legal document." You should also ensure you seeds are geographically distributed so that you will not lose access to at least 3 of them after a large natural disaster. 

### How can I be sure my seed is random? 
Yeti uses Bitcoin Core to generate your randomness. This is the most trustworthy software so it is the only choice for storing significant amounts of bitcoin.

### Any podcasts about the project?
- [McFloogle Episode 171 – Frigid Bitcoin Cold Storage Using Yeti Cold with JW and Will Weatherman](https://www.mcfloogle.com/2019/11/18/episode-171-frigid-bitcoin-cold-storage-using-yeti-cold-with-jw-and-will-weatherman/)

- [The Unhashed Podcast - Cold Storage Done Right (and Wrong) w. JW Weatherman](https://www.stitcher.com/podcast/emissary-ventures-llc/unhashed-podcast/e/76243950)

- [Advanced Tech Podcast Episode 46 - Yeti Cold and Bitcoin Core With JW Weatherman, Will and Robert Spigler](https://advancetechmedia.org/episode-046-weatherman-spigler/)

### Is it dangerous to have all the seeds required for spending on the same laptop at the same time?
No. For Yeti Level 1 and Level 2 you are using a dedicated laptop that has no other software installed outside bitcoin core. This makes it very difficult for an attacker. Seeds are also only on the laptop for a short period of time when spending and then the laptops are erased. For Level 3 seeds are never on a laptop that is internet connected. Level 3 is appropriate for up to 10M USD (in 2018 purchasing power). For amounts over 10M USD Level 4 is under development and will require additional hardware so that two seeds are never on the same device.

### Does Yeti Use Seed Words?
Yes. We use the WIF format and NATO words to make writing down seed words stress free.

### Why doesn't Yeti use Bip39 for Seed Words?
Bip39 is not supported by Bitcoin Core. The bip itself shows that the status of the proposal is that it is "Unanimously Discouraged for Implementation." The reasons for rejecting it fall into two categories. First there are concerns about the cryptographic algorithms used. While the Yeti developers do not understand the details of these concerns because we are not cryptographers we don't see the logic in accepting the risk of using a controversial proposal without gaining any benefit. 

The second set of concerns is around the need to store mappings of words to numbers used in seeds to spend your bitcoin. This is even worse because every human language needs to have a different dictionary and if any of those mappings of words to numbers is lost or corrupted those users will lose all of their stored bitcoin. 

Another problem with Bip39 that was of particular concern to Yeti contributors is that some of the words in Bip39 look similar to one another when hand written. This could create a false sense of security for users that could cause them to lose bitcoin where it would actually be better to have users hand write the letters and numbers they have already learned can be confused for one another.

To solve these problems the Yeti contributors decided that the best solution is to use the well established WIF standard that looks like "abc123" and simply translate those letters and numbers into "alpha bravo charlie ONE TWO THREE." This prevents all of the problems with Bip39. There are no mappings to be lost, the words are very difficult to confuse for other words and the only algorithms involved are universally approved by the smartest cryptographers in bitcoin.



