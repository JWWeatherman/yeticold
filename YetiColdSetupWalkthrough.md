#YetiCold

## This will be a walkthrough of the yeticold setup proccess.

### Step 0
Route name: "https://yeticold.com"

Header: Yeti Bitcoin Cold Storage

Descripton: Choose what version of yeti you want to use.

Action: Click "Yeti cold"

### Step 1
Route name: "https://yeticold.com/Cold/step1"

Header: Gather Required Equipment

Descripton: Gather the required equipment used by yeticold.

Action: Click "Next"

### Step 2
Route name: "https://yeticold.com/Cold/step2"

Header: Install Ubuntu and Label Laptops

Descripton: Install ubuntu on both laptops and label them Primary and Secondary.

Action: Click "Next"

### Step 3
Route name: "https://yeticold.com/Cold/step3"

Header: Switch to your Primary laptop

Descripton: Switch to the laptop you just labeld Primary and go to https://cold.yeticold.com.

Action: Go to "https://cold.yeticold.com"

### Step 4
Route name: "https://yeticold.com/Cold/step4"

Header: Download Yeti to the Primary Laptop

Descripton: Here you will run a command to install the yeti software on your Primary laptop.

Action: Click "Next"

### Step 5
Route name: "https://yeticold.com/Cold/step5"

Header: Start Yeti on your Primary Laptop.

Descripton: Here you run a command that will start the yeticold software.

Action: Run the command on your primary laptop and wait for step 6 to appear.


### Step 6
Route name: "localhost:5000/YCmenu"

Header: Choose to Create or Recover a Yeti Bitcoin Cold Wallet

Descripton: Choose setup or recovery.

Action: Click "Create new yeticold wallet"

### Choose Blockchain 
Route name: "localhost:5000/YCblockchain"

Header: Choose blockchain

Descripton: Choose the blockchain option that best suites your needs.

Action: Click "I don't know the size of my hard drive"

Snapshot: hi

### Step 7
Route name: "localhost:5000/YCopenbitcoin"

Header: Setup your Secondary Laptop.

Descripton: Wait for the chosen blockchain to download while you set up your secondary laptop.

Action: Go to http://disc.yeticold.com on your secondary laptop.

### Step 8
Route name: "https://disc.yeticold.com/Cold/step6"

Header: Start Yeti Cold on your Secondary laptop.

Descripton: Run both commands displayed on the page then wait for step 9 to appear.

Action: Run the commands and wait for step 9.

### Step 9
Route name: "http://localhost:5000/YCopenbitcoinB"

Header: Download the Blockchain.

Descripton: Wait for the blockchain to download then click next.

Action: Click "Next".

### Step 10
Route name: "http://localhost:5000/YCconnection"

Header: Disconnect your Secondary laptop.

Descripton: Disconnect your secondary laptop from all internet sources, we will use network-manager to disable your wifi driver.

Action: Click "Next".


### Step 11
Route name: "http://localhost:5000/YCgetseeds"

Header: Further Randomize Seeds.

Descripton: In this step you can provide random binary that will be used to XOR https://en.wikipedia.org/wiki/Exclusive_or with your bitcoin core generated private keys in order to create 7 secure keys used to generate you multisig wallet. If you do not provide any random binary a binary string consisitng with all 1's will be use instead. This is not a securty risk because the private keys that bitcoin core generates are secure and random. After clicking "Next" we will procide to generate your descriptor that will hold the 7 public keys derived from the private keys.

Action: Click "Next".

### Step 12
Route name: "http://localhost:5000/YCdisplaydescriptor"

Header: Switch to your Primary laptop.

Descripton: Switch your Primary laptop currently displaying step 7 and click Next to continue with step 13. If needed wait until the blockchain finishes downloading before the "Next" button will appear

Action: Click "Next".

### Step 13
Route name: "http://localhost:5000/YCscandescriptor"

Header: Scan the Descriptor from the Secondary laptop.

Descripton: Click the scan button on you Primary button and scan the qr code displayed on you Seconderay laptop.

Action: Click "Scan".


### Step 14
Route name: "http://localhost:5000/YCprintpage"

Header: Print this page.

Descripton: Print the page displayed on your Primary laptop. This page contains you public key descriptor and space for you to wright down you seed later.

Action: Print then click "Next".


### Step 15
Route name: "http://localhost:5000/YCswitchlaptop"

Header: YCswitchlaptop

Descripton: On your Secondary laptop currently showing step 11, click Next and continue on step 16.

Action: Click "Next" on Secondary laptop.


### Step 16-22
Route name: "http://localhost:5000/YCdisplayseeds"

Header: Write Down Private Key X of 7

Descripton: Steps 16-22 will tell you to wright down the words displayed on your screen on the paper that you printed out prevously.

Action: Wright down the words and click "Next".

### Step 23-29
Route name: "http://localhost:5000/YCdisplayseeds"

Header: Check Private Key X of 7

Descripton: Steps 23-29 will tell you to type in the words you just wroute down and yeti will confirm they match what is stored on the laptop.

Action: Type in the words and click "Next".

### Step 30
Route name: "http://localhost:5000/YCcopyseeds"

Header: Copy Seeds to USB drives.

Descripton: After you wrote down the seeds yeti created seven files that each hold you descriptor and your private keys. Move the files into the labeled usb drives.

Action: Move the files and click "Next".

### Step 31
Route name: "http://localhost:5000/YCswitchlaptopB"

Header: Switch to your Primary Laptop

Descripton: On your Primary laptop currently showing step 15, click Next to continue. It will take up to 5 minutes to load the next page.

Action: Click "Next" on your Primary laptop.

### Wallet page
Route name: "http://localhost:5000/YCRdisplaywallet"

Header: Yeti wallet page

Descripton: When you scaned your descriptor on the Primary laptop we derived the watch only addresses from it and displayed them here. You can send and recover funds from here to get started send a test amount to one of the addresses and then follow the on screen instructions to recover it.

Action: Test wallet.
