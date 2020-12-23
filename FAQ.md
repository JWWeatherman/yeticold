## Basics
This FAQ is for "cold" on yeticold.com. The "warm" and "hot" options are less secure, but only require one laptop.

### How much knowledge of Linux is required?
None. You need to be able to follow the tutorials for installing Ubuntu. After Ubuntu is installed you will follow simple instructions until you are done.

### How much time does it take to set up the first time?
The most time consuming part of yeti is waiting for bitcoin core to sync with the network. With an SSD drive this can be done overnight, but if you have an HDD (old style) drive it could take up to a week.

For the part where you are actually doing something it takes less than an hour.

## Hardware

### Does it make sense to get a faster laptop to speed up the process?
Probably not as you will only work with yeti a couple times a year so you won't get a ton of use out of faster hardware. However, an SSD drive is about $50 and makes syncing much faster so if you are a bitcoin enthusiast and you like to test and experiment with bitcoin core it is worth doing.

### What are the minimum specs for the laptops?

Two laptops that can run Ubuntu and Bitcoin Core. At the time of this writing almost any laptop will work but if your laptop has an SSD type hard some steps will take a few hours instead of a few days. Laptops without SSD type drives cost about $150 USD and laptops with SSD drives cost about $200 USD.

You can also buy a chromebook for less than $100, though this hasn't been tested as much and requires a bit of extra work when installing Ubuntu.

### What printer?

You need a printer and printer paper.  The printer will not be used to print out your seed words so it doesn't need to be very secure. 


### When going for a setup with 2 laptops, do the laptops need to be the same?

No.

### What USB sticks are good to get?

Any cheap USB sticks will work fine. 

### Should I try to get a laptop without wifi?

No. Yeti disables your network connections before generating your seed words. It couldn't hurt to have a laptop without wifi or only use your ethernet port for added assurance, but it's probably not worth the hassle.

## Seed

### How to make sure my seed phrases are safe?
They will be written on paper and they are useless unless the attacker gains access to at least 3 of them.

### What about the evil maid attack?
You will store your seed words in multiple, secure, locations. 

### How is this worse than a hardware wallet?

Hardware wallets can be very easy to use because people believe that they are safe even when they plug them into insecure devices like a daily work laptop. This is false, but it does create an easy user experience that is fine for smaller amounts. This also means it is very easy to regularly spend from these devices.

### How is this better than a hardware wallet?
Generic computing hardware is used. Hardware sold specifically for bitcoin storage requires trusting everyone from manufacturing to shipping to fail to realize the opportunity available to modify the hardware in order to steal bitcoin.

When you use a hardware wallet you are trusting the small team of people that write and review the code and everyone that has handled the hardware wallet before you got it. With yeti all important security functions are handled by bitcoin core and it has the best developers and the largest number of people checking for errors. 

You are also using Ubuntu and a generic laptop, but this is more secure as Ubuntu is reviewed by hundreds of developers for security issues and generic hardware makes "supply chain attacks" much more expensive.

### What's a good strategy for storing the seeds?

You can keep more than 1 key in one location. With a 3 out of 7 setup you should never have 3 keys in one location unless you want to transfer. So you need at least 4 locations, one of these can be your home. Other ideas:
- Safety deposit box.
- Your office.
- Store with good friends or family members.
- Accountant
- Lawyer

Always store your seeds with people and locations that do not know they are storing bitcoin seeds. For example your lawyer should believe he is storing "just another important legal document."

### What's the real world risk with having 10MM and only using a Trezor, no multi sig?

The biggest is loss if you don’t have seeds in many locations. The next is theft of a seed phrase. And the next is the risk that your seed isn’t random.

### How can I be sure my seed is random? Can you elaborate on that?

Yeti uses bitcoin core to generate your randomness.

And it uses mulisig so that even if some of your seeds are stolen the bitcoin remains safe.

### The random keys core puts out I can convert into 12 words can't I? Isn't it the same? Wouldn't we just be arguing the randomness of then those 12 words?

You should trust https://github.com/bitcoin/bitcoin  to create your random words that secure your bitcoin more than anything else.


## Any podcasts about the project?

- [McFloogle Episode 171 – Frigid Bitcoin Cold Storage Using Yeti Cold with JW and Will Weatherman](https://www.mcfloogle.com/2019/11/18/episode-171-frigid-bitcoin-cold-storage-using-yeti-cold-with-jw-and-will-weatherman/)

- [The Unhashed Podcast - Cold Storage Done Right (and Wrong) w. JW Weatherman](https://www.stitcher.com/podcast/emissary-ventures-llc/unhashed-podcast/e/76243950)
