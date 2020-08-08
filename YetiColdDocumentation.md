# Yeticold

## Overview

Yeticold is the most secure of the three yeti applications. It uses:
  1. A 3 of 7 multisig wallet.
  1. An offline laptop to handle sensitive data.
  1. QR codes to transfer public key data from the offline laptop.
  1. Seven USB and paper copies of your seeds.
  
## Wallet Creation

### These steps are entirly done on the offline machine:
Yeticold uses these steps to generate your private seeds:
  1. We ask bitcoin core to generate seven private key in the WIF format. 
  1. We convert the bitcoin core keys into a 256 binary string.
  1. We ask the user to provide random data in the form of seven sets of 256 binary numbers.
     1. We suggest using dice to get purly random data to further randomise your private keys.
     1. If the user dose not want to provide random binary data we use a set string of binary.
     1. While it will not increse the security by chosing this, it will also not reduce the secrutiy of the original seven bitcoin generated keys either.
  1. We XOR the seven sets of two 256 binary strings to get a different key then the originaly generate bitcoin keys.
  1. We convert the new seven binary strings back into WIF format.
  1. After we finish creating your wallet we convert the seven WIF keys into the NATO format we use to store your keys.
  
### These steps are entirly done on the offline machine:
Yeticold uses these steps to generate your wallet from your private keys:
  1. We import your WIF keys into bitcoin core using the sethdsead rpc command.
  1. We get your xpriv that was generated when you imported your WIF key to bitcoin core using the dump wallet rpc command.
  1. We generate a descriptor using your xpriv.
     1. This is an example of what your xprv descriptor will look like "wsh(multi(xprv1...,xprv2...,xprv3...,xprv4...,xprv5...,xprv6...,xprv7...))".
  1. We can the get your xpub keys by using getdescriptorinfo rpc command on your xprv descriptor.
     1. This is an example of what your xpup descriptor will look like "wsh(multi(xpub1...,xpub2...,xpub3...,xpub4...,xpub5...,xpub6...,xpub7...))".
  1. We then import 1000 addresses from your xprv descriptor.
     1. The number 1000 is almost entiraly arbitrary and is just the number of addreses we import from your xprv descirptor.
     1. This number can also be changed at any time if you run out of addresses to use years later.
     1. The reason for importing your keys to your offline machine is to save time when you later send from your offline machine in the recover process.
     
### These steps use your offline and online machine:
Yeticold uses these steps to get your recovery data into your seven seed packets:
  1. We send your xpub descriptor over to your online laptop using a QR code.
     1. You are going to use QR codes for this steps to transfer data accross you machines. You should scan the QR code using another reader, like a phone app, to confirm that no critical data is being transfered to an online machine.
     1. Your xpub descriptor if stolen can be used to see your addreses and the balance stored on them, but it cannot be used to help crack you xprv.
     1. The only downside of letting your xpub descriptor get out is it will reduce your anonymity and provide motivation for hackers to target you and the software your using.
  1. On your online laptop you will then print out sevral pages that hold your xpub descriptor and space to wright out your xprv keys in the NATO format.
  1. We display your xprv keys in NATO format on you offline machine, you will need to wright down these words onto the paper that you printed out.
  1. You can optinal connect the 7 USB drives to your offline machine.
     1. You will transfer a file that contains your your xpub descriptor and your xprv keys in NATO format to the usb drives.
     1. Using USB drives will allow you to skip the process of typing in a hundred plus words when ever you want to recover.
     1. This dose reduce securtiy if the USB drives have a wifi card installed or you acidently plug them into a wifi enabled laptop.
     1. This functionality is mostly suggusted for yetiwarm where you will need to recover more often and don't want to type the words in every week.
  1. You will need to store the paper and USB seed pairs in seven different locations.
     1. Because your wallet is a 3 of 7 you can have a seed packet sent to an unsecure location like a lawer or such if you want to have a secure 2 of 7 wallet if you think you might loose 4 of the 7 seed packets.
