### How can I get an overview of Yeti?
The first step on each level of Yeti provides a link to a complete video walk through. Grab some popcorn and enjoy.

Level 1
https://yeticold.com/Hot/step1

Level 2
https://yeticold.com/Warm/step1

Level 3
https://yeticold.com/Cold/step1

### How much knowledge of Linux is required?
None. Installing Ubuntu is the only challenging task and it is no more difficult than installing Windows or Mac OS. Even if you have never installed an OS before it is not difficult and you can get support from our slack channel at:

https://join.slack.com/t/yeticold/shared_invite/zt-hisfxrra-BZzrYCDnqFv6whxVn~6FQQ

You can also hire a local computer shop to install Ubuntu for you for about $30 and as long as they don't suspect you will use this laptop for bitcoin it is a reasonably safe option.

### How much time does it take to set up the first time?
The most time consuming part of yeti is waiting for bitcoin core to sync with the network. With an SSD drive this can be done overnight, but if you have an HDD (old style) drive it could take up to a week.

For the part where you are actually doing something it takes less than an hour.

## Hardware

### Does it make sense to get a faster laptop to speed up the process?
Probably not as you will only work with yeti a couple times a year so you won't get a ton of use out of faster hardware. However, an SSD drive is about $50 and makes syncing much faster so if you are a bitcoin enthusiast and you like to test and experiment with bitcoin core it is worth doing.

### What are the minimum specs for the laptops?
A laptop(s) that can run Ubuntu and Bitcoin Core is required. At the time of this writing almost any laptop will work but if your laptop has an SSD type hard drive some steps will take a few hours instead of a few days. Laptops without SSD type drives cost about $150 USD and laptops with SSD drives cost about $200 USD.

### Why do I need a printer?
You only need a printer for Level 3 and it is used to print out recovery instructions. The printer will be used to print your seed words.

### When using Level 3 it requires two laptops, do the laptops need to be the same?
No. Any laptops that can run Ubuntu and Bitcoin core will work great.

### What USB sticks are good to get?
Any cheap USB sticks will work fine. 

### Should I try to get a laptop without wifi?
No. Yeti disables your network connections before generating your seed words. It couldn't hurt to have a laptop without wifi or only use your Ethernet port for added assurance, but it's probably not worth the hassle.

## Seed

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

## Any podcasts about the project?
- [McFloogle Episode 171 – Frigid Bitcoin Cold Storage Using Yeti Cold with JW and Will Weatherman](https://www.mcfloogle.com/2019/11/18/episode-171-frigid-bitcoin-cold-storage-using-yeti-cold-with-jw-and-will-weatherman/)

- [The Unhashed Podcast - Cold Storage Done Right (and Wrong) w. JW Weatherman](https://www.stitcher.com/podcast/emissary-ventures-llc/unhashed-podcast/e/76243950)

- [Advanced Tech Podcast Episode 46 - Yeti Cold and Bitcoin Core With JW Weatherman, Will and Robert Spigler](https://advancetechmedia.org/episode-046-weatherman-spigler/)
