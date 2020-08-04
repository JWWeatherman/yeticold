#YetiCold

## This will be a walkthrough of the yeticold setup proccess.

### Step 0
Route name: "https://yeticold.com"

Header: Yeti Bitcoin Cold Storage

Descripton: Here you will choose what version of yeti you will be setting up.

Yeti Cold: Yeticold is the most secure version of yeti and uses a 3 of 7 multisig for your wallet and has two laptops Primary(Online) and Secondary(Offline). After downloading some librarys and the bitcoin block chain the Secondary laptop is disconnected from the internet. You will the use qr codes to transfer data between the two machines completly removing the ability for a viruse to send vital information off of the Secondary(Offline) Machine. 

Yeti Warm: A less secure version of YetiCold where you only use one machine which is Online but is still a 3 of 7 multisig.

Yeti Hot: A very simple app that uses Yeti's NATO seed format and creates a single key wallet from bitcoin core. You use bitcoin core as an interface for sending and reciving.

Action: Click "Yeti cold"

Code: https://github.com/JWWeatherman/yetihosted

### Step 1
Route name: "https://yeticold.com/Cold/step1"

Header: Gather Required Equipment

Descripton: You will need verying amounts of equipment depending on the version of yeti your using. For this walkthrough we are using yeticold so you will need:

1. Two laptops that will later have ubuntu installed on them.
2. 7 usb sticks to store the digital version of your NATO seeds.
3. A printer and paper to store the paper version of your NATO seeds.

Action: Click "Next"

Code: https://github.com/JWWeatherman/yetihosted

### Step 2
Route name: "https://yeticold.com/Cold/step2"

Header: Install Ubuntu and Label Laptops

Descripton: Here you will need to install ubuntu on both of the laptops you can use this tutorial here.

Tutorial: https://tutorials.ubuntu.com/tutorial/tutorial-install-ubuntu-desktop#0

Action: Click "Next"

Code: https://github.com/JWWeatherman/yetihosted

### Step 3
Route name: "https://yeticold.com/Cold/step3"

Header: Switch to your Primary laptop

Descripton: Now you will procide to setup your Primary laptop with yeti, to start go to https://yeticold.com.

Action: Go to "https://cold.yeticold.com"

Code: https://github.com/JWWeatherman/yetihosted

### Step 4
Route name: "https://yeticold.com/Cold/step4"

Header: Download Yeti to the Primary Laptop

Descripton: This command will install github's git https://github.com/git/git and then use git to clone the yeticold repo https://github.com/JWWeatherman/yeticold.

Command: sudo apt-get update; sudo apt-get install git; git clone https://github.com/jwweatherman/yeticold.git ~/yeticold

Action: Click "Next"

Code: https://github.com/JWWeatherman/yetihosted

### Step 5
Route name: "https://yeticold.com/Cold/step5"

Header: Start Yeti on your Primary Laptop.

Descripton: Now you will run the command that will start up yeti in your browser.

Command: python3 ~/yeticold/scripts/YetiCold.py

Issues: Sometimes yeticold will not show up in your browser or it will give an error in the browser. To fix open your browser and/or refresh the page.

Action: Run the command on your primary laptop and wait for step 6 to appear.

Code: https://github.com/JWWeatherman/yetihosted

### Step 6
Route name: "localhost:5000/YCmenu"

Header: Choose to Create or Recover a Yeti Bitcoin Cold Wallet

Descripton: You can choose to Create a new wallet or Recover and existing one.

Action: Click "Create new yeticold wallet"

Code: https://github.com/JWWeatherman/yeticold/blob/ac6981e1925766659cc08c3ccbdf7dbc4517339f/appyeticold.py#L103

### Choose Blockchain 
Route name: "localhost:5000/YCblockchain"

Header: Choose blockchain

Descripton: Choose the blockchain option that best suites your needs. If you have a small hard drive you have to prune https://www.reddit.com/r/Bitcoin/comments/5ywru2/what_is_the_prune_mode_exactly/ the bitcoin blockchain in order to store it on your machine. Its better if you have an unpruned node because you won't have to redownload it when you want to recover from a point farther in the past then the 550 block pruneing, so if you click I have a large hard drive we will not prune the blockchain. I don't know the size of my hard drive defaults to small hard drive.

Test Block Chain: The test block chain is a pruned blockchain that willweatherman has stored in his google drive. Because it is not downloaded from the network it is not trustworthy for recording balances. It is perfectly fine for sending small amounts around for testing purposes and save a signifigant amount of time to download.

Issue: If you don't see this page and it skips to YCopenbitcoin(step 7) it is because you already have a blockchain that bitcoin core can use and yeti will proceed to update it.

Action: Click "I don't know the size of my hard drive"

Code: https://github.com/JWWeatherman/yeticold/blob/ac6981e1925766659cc08c3ccbdf7dbc4517339f/appyeticold.py#L690

### Step 7
Route name: "localhost:5000/YCopenbitcoin"

Header: Setup your Secondary Laptop.

Descripton: While yeti is downloading or updating the bitcoin blockchain that you choose in the previous screen, You will switch to your Secondary laptop and set it up.

Action: Go to http://disc.yeticold.com on your secondary laptop.

Code: https://github.com/JWWeatherman/yeticold/blob/ac6981e1925766659cc08c3ccbdf7dbc4517339f/appyeticold.py#L729

### Step 8
Route name: "https://disc.yeticold.com/Cold/step6"

Header: Start Yeti Cold on your Secondary laptop.

Descripton: Run these same two commands shown preveously on your Secondary laptop to download and run yeti.

Issues: Sometimes yeticold will not show up in your browser or it will give an error in the browser. To fix open your browser and/or refresh the page.

Action: Run the commands and wait for step 9.

Code: https://github.com/JWWeatherman/yetihosted

### Step 9
Route name: "http://localhost:5000/YCopenbitcoinB"

Header: Download the Blockchain.

Descripton: Wait for the blockchain to download then click next, this step could take a signifigant amount of time. Because this is the offline machine and is not going to send or recive, we will download the testblockchain mentioned prevously to save time.

Action: Click "Next".

Code: https://github.com/JWWeatherman/yeticold/blob/ac6981e1925766659cc08c3ccbdf7dbc4517339f/appyeticold.py#L220

### Step 10
Route name: "http://localhost:5000/YCconnection"

Header: Disconnect your Secondary laptop.

Descripton: Disconnect your secondary laptop from all internet sources, we will use network-manager to disable your wifi driver.

Action: Click "Next".

Code: https://github.com/JWWeatherman/yeticold/blob/ac6981e1925766659cc08c3ccbdf7dbc4517339f/appyeticold.py#L243

### Step 11
Route name: "http://localhost:5000/YCgetseeds"

Header: Further Randomize Seeds.

Descripton: In this step you can provide random binary that will be used to XOR https://en.wikipedia.org/wiki/Exclusive_or with your bitcoin core generated private keys in order to create 7 secure keys used to generate you multisig wallet. If you do not provide any random binary a binary string consisitng with all 1's will be use instead. This is not a securty risk because the private keys that bitcoin core generates are secure and random. After clicking "Next" we will proceed to generate your descriptor that will hold the 7 public keys derived from the private keys.

Action: Click "Next".

Code: https://github.com/JWWeatherman/yeticold/blob/ac6981e1925766659cc08c3ccbdf7dbc4517339f/appyeticold.py#L823

### Step 12
Route name: "http://localhost:5000/YCdisplaydescriptor"

Header: Switch to your Primary laptop.

Descripton: Switch your Primary laptop currently displaying step 7 and click Next to continue with step 13. If needed wait until the blockchain finishes downloading before the "Next" button will appear

Action: Click "Next".

Code: https://github.com/JWWeatherman/yeticold/blob/ac6981e1925766659cc08c3ccbdf7dbc4517339f/appyeticold.py#L898

### Step 13
Route name: "http://localhost:5000/YCscandescriptor"

Header: Scan the Descriptor from the Secondary laptop.

Descripton: Click the scan button on you Primary button and scan the qr code displayed on you Seconderay laptop.

Action: Click "Scan".

Code: https://github.com/JWWeatherman/yeticold/blob/ac6981e1925766659cc08c3ccbdf7dbc4517339f/appyeticold.py#L921

### Step 14
Route name: "http://localhost:5000/YCprintpage"

Header: Print this page.

Descripton: Print the page displayed on your Primary laptop. This page contains you public key descriptor and space for you to wright down you seed later.

Action: Print then click "Next".

Code: https://github.com/JWWeatherman/yeticold/blob/ac6981e1925766659cc08c3ccbdf7dbc4517339f/appyeticold.py#L932

### Step 15
Route name: "http://localhost:5000/YCswitchlaptop"

Header: YCswitchlaptop

Descripton: On your Secondary laptop currently showing step 11, click Next and continue on step 16.

Action: Click "Next" on Secondary laptop.

Code: https://github.com/JWWeatherman/yeticold/blob/ac6981e1925766659cc08c3ccbdf7dbc4517339f/appyeticold.py#L956s

### Step 16-22
Route name: "http://localhost:5000/YCdisplayseeds"

Header: Write Down Private Key X of 7

Descripton: Steps 16-22 will tell you to wright down the words displayed on your screen on the paper that you printed out prevously. This step will also create files in your Documents folder that each contain your public key descriptor and one of your seeds.

Action: Wright down the words and click "Next".

Code: https://github.com/JWWeatherman/yeticold/blob/ac6981e1925766659cc08c3ccbdf7dbc4517339f/appyeticold.py#L962

### Step 23-29
Route name: "http://localhost:5000/YCdisplayseeds"

Header: Check Private Key X of 7

Descripton: Steps 23-29 will tell you to type in the words you just wroute down and yeti will confirm they match what is stored on the laptop.

Action: Type in the words and click "Next".

Code: https://github.com/JWWeatherman/yeticold/blob/ac6981e1925766659cc08c3ccbdf7dbc4517339f/appyeticold.py#L1012

### Step 30
Route name: "http://localhost:5000/YCcopyseeds"

Header: Copy Seeds to USB drives.

Descripton: After you wrote down the seeds yeti created seven files that each hold you descriptor and your private keys. Move the files into the labeled usb drives. You will store the matching usb/paper seed pairs in seven diffrent locations.

Action: Move the files and click "Next".

Code: https://github.com/JWWeatherman/yeticold/blob/ac6981e1925766659cc08c3ccbdf7dbc4517339f/appyeticold.py#L1071

### Step 31
Route name: "http://localhost:5000/YCswitchlaptopB"

Header: Switch to your Primary Laptop

Descripton: On your Primary laptop currently showing step 15, click Next to continue. It will take up to 5 minutes to load the next page.

Action: Click "Next" on your Primary laptop.

Code: https://github.com/JWWeatherman/yeticold/blob/ac6981e1925766659cc08c3ccbdf7dbc4517339f/appyeticold.py#L1077

### Wallet page
Route name: "http://localhost:5000/YCRdisplaywallet"

Header: Yeti wallet page

Descripton: When you scaned your descriptor on the Primary laptop we derived the watch only addresses from it and displayed them here. You can send and recover funds from here to get started send a test amount to one of the addresses and then follow the on screen instructions to recover it.

Action: Test wallet.

Code: https://github.com/JWWeatherman/yeticold/blob/ac6981e1925766659cc08c3ccbdf7dbc4517339f/appyeticold.py#L281
