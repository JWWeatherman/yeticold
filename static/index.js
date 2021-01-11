var navbar = (yeti='Cold', url) => {
  if (yeti == 'Warm') {
    document.getElementById('navbar').innerHTML = '<nav class="form-row navbar navbar-light bg-warning"><img src="'+url+'" width="50" height="50" class="align-top" alt=""><h3 style="color:black;margin:0;">Yeti Level 2 Wallet</h3></nav>';
  } else if (yeti == 'Hot') {
    document.getElementById('navbar').innerHTML = '<nav class="form-row navbar navbar-light bg-danger"><img src="'+url+'" width="50" height="50" class="align-top" alt=""><h3 style="color:white;margin:0;">Yeti Level 1 Wallet</h3></nav>';
  } else if (yeti == 'BCO') {
    document.getElementById('navbar').innerHTML = '<nav class="form-row navbar navbar-light bg-info"><img src="'+url+'" width="50" height="50" class="align-top" alt=""><h3 style="color:blac;margin:0;">Bitcoin Core Offline</h3></nav>';
  } else {
    document.getElementById('navbar').innerHTML = '<nav class="form-row navbar navbar-light bg-primary"><img src="'+url+'" width="50" height="50" class="align-top" alt=" "><h3 style="color:white;margin:0;">Yeti Level 3 Wallet</h3></nav>';
  }
}

var autocompletelist = {
    "ON": "ONE",
    "ONE": "ONE",
    "TW": "TWO",
    "TWO": "TWO",
    "TH": "THREE",
    "THR": "THREE",
    "THRE": "THREE",
    "THREE": "THREE",
    "FOU": "FOUR",
    "FOUR": "FOUR",
    "FI": "FIVE",
    "FIV": "FIVE",
    "FIVE": "FIVE",
    "SIX": "SIX",
    "SE": "SEVEN",
    "SEV": "SEVEN",
    "SEVE": "SEVEN",
    "SEVEN": "SEVEN",
    "EI": "EIGHT",
    "EIG": "EIGHT",
    "EIGH": "EIGHT",
    "EIGHT": "EIGHT",
    "NI": "NINE",
    "NIN": "NINE",
    "NINE": "NINE",
    "A": "ALFA",
    "AL": "ALFA",
    "ALF": "ALFA",
    "ALFA": "ALFA",
    "B": "BRAVO",
    "BR": "BRAVO",
    "BRA": "BRAVO",
    "BRAV": "BRAVO",
    "BRAVO": "BRAVO",
    "C": "CHARLIE",
    "CH": "CHARLIE",
    "CHA": "CHARLIE",
    "CHAR": "CHARLIE",
    "CHARL": "CHARLIE",
    "CHARLI": "CHARLIE",
    "CHARLIE": "CHARLIE",
    "D": "DELTA",
    "DE": "DELTA",
    "DEL": "DELTA",
    "DELT": "DELTA",
    "DELTA": "DELTA",
    "EC": "ECHO",
    "ECH": "ECHO",
    "ECHO": "ECHO",
    "FOX": "FOXTROT",
    "FOXT": "FOXTROT",
    "FOXTR": "FOXTROT",
    "FOXTRO": "FOXTROT",
    "FOXTROT": "FOXTROT",
    "G": "GOLF",
    "GO": "GOLF",
    "GOL": "GOLF",
    "GOLF": "GOLF",
    "H": "HOTEL",
    "HO": "HOTEL",
    "HOT": "HOTEL",
    "HOTE": "HOTEL",
    "HOTEL": "HOTEL",
    "I": "INDIA",
    "IN": "INDIA",
    "IND": "INDIA",
    "INDI": "INDIA",
    "INDIA": "INDIA",
    "J": "JULIETT",
    "JU": "JULIETT",
    "JUL": "JULIETT",
    "JULI": "JULIETT",
    "JULIE": "JULIETT",
    "JULIET": "JULIETT",
    "JULIETT": "JULIETT",
    "K": "KILO",
    "KI": "KILO",
    "KIL": "KILO",
    "KILO": "KILO",
    "L": "LIMA",
    "LI": "LIMA",
    "LIM": "LIMA",
    "LIMA": "LIMA",
    "M": "MIKE",
    "MI": "MIKE",
    "MIK": "MIKE",
    "MIKE": "MIKE",
    "NO": "NOVEMBER",
    "NOV": "NOVEMBER",
    "NOVE": "NOVEMBER",
    "NOVEM": "NOVEMBER",
    "NOVEMB": "NOVEMBER",
    "NOVEMBE": "NOVEMBER",
    "NOVEMBER": "NOVEMBER",
    "OS": "OSCAR",
    "OSC": "OSCAR",
    "OSCA": "OSCAR",
    "OSCAR": "OSCAR",
    "P": "PAPA",
    "PA": "PAPA",
    "PAP": "PAPA",
    "PAPA": "PAPA",
    "Q": "QUEBEC",
    "QU": "QUEBEC",
    "QUE": "QUEBEC",
    "QUEB": "QUEBEC",
    "QUEBE": "QUEBEC",
    "QUEBEC": "QUEBEC",
    "R": "ROMEO",
    "RO": "ROMEO",
    "ROM": "ROMEO",
    "ROME": "ROMEO",
    "ROMEO": "ROMEO",
    "SIE": "SIERRA",
    "SIER": "SIERRA",
    "SIERR": "SIERRA",
    "SIERRA": "SIERRA",
    "TA": "TANGO",
    "TAN": "TANGO",
    "TANG": "TANGO",
    "TANGO": "TANGO",
    "U": "UNIFORM",
    "UN": "UNIFORM",
    "UNI": "UNIFORM",
    "UNIF": "UNIFORM",
    "UNIFO": "UNIFORM",
    "UNIFOR": "UNIFORM",
    "UNIFORM": "UNIFORM",
    "V": "VICTOR",
    "VI": "VICTOR",
    "VIC": "VICTOR",
    "VICT": "VICTOR",
    "VICTO": "VICTOR",
    "VICTOR": "VICTOR",
    "W": "WHISKEY",
    "WH": "WHISKEY",
    "WHI": "WHISKEY",
    "WHIS": "WHISKEY",
    "WHISK": "WHISKEY",
    "WHISKE": "WHISKEY",
    "WHISKEY": "WHISKEY",
    "X": "X-RAY",
    "X-": "X-RAY",
    "X-R": "X-RAY",
    "X-RA": "X-RAY",
    "X-RAY": "X-RAY",
    "Y": "YANKEE",
    "YA": "YANKEE",
    "YAN": "YANKEE",
    "YANK": "YANKEE",
    "YANKE": "YANKEE",
    "YANKEE": "YANKEE",
    "Z": "ZULU",
    "ZU": "ZULU",
    "ZUL": "ZULU",
    "ZULU": "ZULU",
    "a": "alfa",
    "al": "alfa",
    "alf": "alfa",
    "alfa": "alfa",
    "b": "bravo",
    "br": "bravo",
    "bra": "bravo",
    "brav": "bravo",
    "bravo": "bravo",
    "c": "charlie",
    "ch": "charlie",
    "cha": "charlie",
    "char": "charlie",
    "charl": "charlie",
    "charli": "charlie",
    "charlie": "charlie",
    "d": "delta",
    "de": "delta",
    "del": "delta",
    "delt": "delta",
    "delta": "delta",
    "e": "echo",
    "ec": "echo",
    "ech": "echo",
    "echo": "echo",
    "f": "foxtrot",
    "fo": "foxtrot",
    "fox": "foxtrot",
    "foxt": "foxtrot",
    "foxtr": "foxtrot",
    "foxtro": "foxtrot",
    "foxtrot": "foxtrot",
    "g": "golf",
    "go": "golf",
    "gol": "golf",
    "golf": "golf",
    "h": "hotel",
    "ho": "hotel",
    "hot": "hotel",
    "hote": "hotel",
    "hotel": "hotel",
    "i": "india",
    "in": "india",
    "ind": "india",
    "indi": "india",
    "india": "india",
    "j": "juliett",
    "ju": "juliett",
    "jul": "juliett",
    "juli": "juliett",
    "julie": "juliett",
    "juliet": "juliett",
    "juliett": "juliett",
    "k": "kilo",
    "ki": "kilo",
    "kil": "kilo",
    "kilo": "kilo",
    "l": "lima",
    "li": "lima",
    "lim": "lima",
    "lima": "lima",
    "m": "mike",
    "mi": "mike",
    "mik": "mike",
    "mike": "mike",
    "n": "november",
    "no": "november",
    "nov": "november",
    "nove": "november",
    "novem": "november",
    "novemb": "november",
    "novembe": "november",
    "november": "november",
    "o": "oscar",
    "os": "oscar",
    "osc": "oscar",
    "osca": "oscar",
    "oscar": "oscar",
    "p": "papa",
    "pa": "papa",
    "pap": "papa",
    "papa": "papa",
    "q": "quebec",
    "qu": "quebec",
    "que": "quebec",
    "queb": "quebec",
    "quebe": "quebec",
    "quebec": "quebec",
    "r": "romeo",
    "ro": "romeo",
    "rom": "romeo",
    "rome": "romeo",
    "romeo": "romeo",
    "s": "sierra",
    "si": "sierra",
    "sie": "sierra",
    "sier": "sierra",
    "sierr": "sierra",
    "sierra": "sierra",
    "t": "tango",
    "ta": "tango",
    "tan": "tango",
    "tang": "tango",
    "tango": "tango",
    "u": "uniform",
    "un": "uniform",
    "uni": "uniform",
    "unif": "uniform",
    "unifo": "uniform",
    "unifor": "uniform",
    "uniform": "uniform",
    "v": "victor",
    "vi": "victor",
    "vic": "victor",
    "vict": "victor",
    "victo": "victor",
    "victor": "victor",
    "w": "whiskey",
    "wh": "whiskey",
    "whi": "whiskey",
    "whis": "whiskey",
    "whisk": "whiskey",
    "whiske": "whiskey",
    "whiskey": "whiskey",
    "x": "x-ray",
    "x-": "x-ray",
    "x-r": "x-ray",
    "x-ra": "x-ray",
    "x-ray": "x-ray",
    "y": "yankee",
    "ya": "yankee",
    "yan": "yankee",
    "yank": "yankee",
    "yanke": "yankee",
    "yankee": "yankee",
    "z": "zulu",
    "zu": "zulu",
    "zul": "zulu",
    "zulu": "zulu"
  } 
  var multiautocompletelist = {
    "F":"FOUR\nFIVE\nFOXTROT",
    "S":"SIERRA\nSIX\nSEVEN",
    "T":"TWO\nTHREE\nTANGO",
    "N":"NINE\nNOVEMBER",
    "FO":"FOUR\nFOXTROT",
    "SI":"SIERRA\nSIX",
    "E":"EIGHT\nECHO",
    "O":"ONE\nOSCAR"
  }
  var switcher = {
  "1": "ONE",
  "2": "TWO",
  "3": "THREE",
  "4": "FOUR",
  "5": "FIVE",
  "6": "SIX",
  "7": "SEVEN",
  "8": "EIGHT",
  "9": "NINE",
  "A": "ALFA",
  "B": "BRAVO",
  "C": "CHARLIE",
  "D": "DELTA",
  "E": "ECHO",
  "F": "FOXTROT",
  "G": "GOLF",
  "H": "HOTEL",
  "I": "INDIA",
  "J": "JULIETT",
  "K": "KILO",
  "L": "LIMA",
  "M": "MIKE",
  "N": "NOVEMBER",
  "O": "OSCAR",
  "P": "PAPA",
  "Q": "QUEBEC",
  "R": "ROMEO",
  "S": "SIERRA",
  "T": "TANGO",
  "U": "UNIFORM",
  "V": "VICTOR",
  "W": "WHISKEY",
  "X": "X-RAY",
  "Y": "YANKEE",
  "Z": "ZULU",
  "a": "alfa",
  "b": "bravo",
  "c": "charlie",
  "d": "delta",
  "e": "echo",
  "f": "foxtrot",
  "g": "golf",
  "h": "hotel",
  "i": "india",
  "j": "juliett",
  "k": "kilo",
  "l": "lima",
  "m": "mike",
  "n": "november",
  "o": "oscar",
  "p": "papa",
  "q": "quebec",
  "r": "romeo",
  "s": "sierra",
  "t": "tango",
  "u": "uniform",
  "v": "victor",
  "w": "whiskey",
  "x": "x-ray",
  "y": "yankee",
  "z": "zulu",
  "ONE": "1",
  "TWO": "2",
  "THREE": "3",
  "FOUR": "4",
  "FIVE": "5",
  "SIX": "6",
  "SEVEN": "7",
  "EIGHT": "8",
  "NINE": "9",
  "ALFA": "A",
  "BRAVO": "B",
  "CHARLIE": "C",
  "DELTA": "D",
  "ECHO": "E",
  "FOXTROT": "F",
  "GOLF": "G",
  "HOTEL": "H",
  "INDIA": "I",
  "JULIETT": "J",
  "KILO": "K",
  "LIMA": "L",
  "MIKE": "M",
  "NOVEMBER": "N",
  "OSCAR": "O",
  "PAPA": "P",
  "QUEBEC": "Q",
  "ROMEO": "R",
  "SIERRA": "S",
  "TANGO": "T",
  "UNIFORM": "U",
  "VICTOR": "V",
  "WHISKEY": "W",
  "X-RAY": "X",
  "YANKEE": "Y",
  "ZULU": "Z",
  "alfa": "a",
  "bravo": "b",
  "charlie": "c",
  "delta": "d",
  "echo": "e",
  "foxtrot": "f",
  "golf": "g",
  "hotel": "h",
  "india": "i",
  "juliett": "j",
  "kilo": "k",
  "lima": "l",
  "mike": "m",
  "november": "n",
  "oscar": "o",
  "papa": "p",
  "quebec": "q",
  "romeo": "r",
  "sierra": "s",
  "tango": "t",
  "uniform": "u",
  "victor": "v",
  "whiskey": "w",
  "x-ray": "x",
  "yankee": "y",
  "zulu": "z"
}
var BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
var base_count = BASE58_ALPHABET.length
var passphraseWIFlist = ['ONE','TWO','THREE','FOUR','FIVE','SIX','SEVEN','EIGHT','NINE','alfa','bravo','charlie','delta','echo','foxtrot','golf','hotel','india','juliett','kilo','lima','mike','oscar','november','papa','quebec','romeo','sierra','tango','uniform','victor','whiskey','x-ray','yankee','zulu','ALFA','BRAVO','CHARLIE','DELTA','ECHO','FOXTROT','GOLF','HOTEL','INDIA','JULIETT','KILO','LIMA','MIKE','OSCAR','NOVEMBER','PAPA','QUEBEC','ROMEO','SIERRA','TANGO','UNIFORM','VICTOR','WHISKEY','X-RAY','YANKEE','ZULU']

var hashFour = (passphraselist) => {
  var hash = CryptoJS.SHA256(PassphraseToWIF(passphraselist)).toString(CryptoJS.enc.Hex)
  var mod = parseInt(BigInt('0x' + hash) % BigInt(58))
  var char = BASE58_ALPHABET.charAt(mod)
  return WIFToPassphrase(char)[0]
}

var decode = (s) => {
  var decoded = 0
  var multi = 1
  var news = s.split('').reverse().join().replace(',','').replace(',','').replace(',','').replace(',','')
  for (char in news) {
    decoded = decoded + (multi * BASE58_ALPHABET.indexOf(news.charAt(char)))
    multi = multi * base_count
  }
  return decoded
}

var makechecksum = (passphraselist) => {
  var list = PassphraseToWIF(passphraselist)
  var sum = 0
  for (char in list) {
    var decodenum = decode(list.charAt(char))
    sum = sum + decodenum
  }
  mod = sum % 58
  var char = BASE58_ALPHABET.charAt(mod)
  char = WIFToPassphrase(char)[0]
  return char
}

var checksum = () => {
  for (var i = 1; i < 14; i++) {
    var fourwords = document.getElementById('displayrow' + i).value.split(' ')
    var Letter = makechecksum(fourwords)
    document.getElementById('displayrow' + i).value = document.getElementById('displayrow' + i).value + ' ' + Letter
  }
}
  
var CheckSumMatch = (passphraselist, checksum) => {
   var list = PassphraseToWIF(passphraselist)
   var sum = 0
   for (char in list) {
     var decodenum = decode(list.charAt(char))
     sum = sum + decodenum
   }
   mod = sum % 58
   var char = BASE58_ALPHABET.charAt(mod)
   char = WIFToPassphrase(char)[0]
   return char === checksum
 }

 var PassphraseToWIF = (passphraselist) => {
   var WIFlist = ''
   for(var i = 0; i < passphraselist.length; i++) {
     var WIF = switcher[passphraselist[i]]
     WIFlist = WIFlist + WIF
   }
   return WIFlist
 }

 var WIFToPassphrase = (WIFString) => {
   var passphraselist = []
   for(var i = 0; i < WIFString.length; i++) {
     var passphrase = switcher[WIFString.charAt(i)]
     passphraselist.push(passphrase)
   }
   return passphraselist
 }

 var highlightrows = () => {
   var templist = []
   var numofrowsgreen = 0
   var red = "rgba(255, 0, 0, 0.4)"
   var green = "rgba(0, 151, 19, 0.4)"
   for(var i = 1;i < 14; i++) {
     document.getElementById('row' + i).style.backgroundColor = ""
     templist = document.getElementById('row' + i).value.toString().split(' ')
     var checksum = templist.pop()
     if (document.getElementById('row' + i).value) document.getElementById('row' + i).style.backgroundColor = red
     if (templist.filter((el) => {return passphraseWIFlist.includes(el)}).length === 4) {
       if (checksum != '') {
         if (CheckSumMatch(templist,checksum)) {
           numofrowsgreen++
           document.getElementById('row' + i).style.backgroundColor = green
         }
       }
       templist = []
     }
   }
   var ConvertKey = numofrowsgreen === 13
   if (ConvertKey) {
     document.getElementById("nextkey").disabled = false
   } else {
     document.getElementById("nextkey").disabled = true
   }
   setTimeout(() => { highlightrows() }, 80)
 }

 var autocomplete = (input) => {
   inputs = input.split(' ')
   if (autocompletelist[inputs[inputs.length - 1]] != undefined) {
     inputs[inputs.length - 1] = autocompletelist[inputs[inputs.length - 1]]
     inputs = inputs.join(' ')
   } else {
     inputs = false
   }
   return inputs
 }

 var autocompletetooltip = (input) => {
   inputs = input.split(' ')
   tooltip = ''
   if (autocompletelist[inputs[inputs.length - 1]] != undefined) {
     tooltip = autocompletelist[inputs[inputs.length - 1]]
   } else {
     tooltip = multiautocompletelist[inputs[inputs.length - 1]]
   }
   return tooltip
 }

var importfile = (yeti) => {
  let file = document.getElementById("filepath").files[0]
  if (file != undefined) {
    let reader = new FileReader()
    document.getElementById('filepath').value = ""
    if (yeti !== 'Hot'){
      reader.onload = function(evt) {
        let list = evt.target.result.toString().split('\n')
        document.getElementById('descriptor').value = list[16] 
        for (let i = 0; i <= 12; i++) {
          document.getElementById('row' + (i+1)).value = list[i]
        }
      }
    } else {
      reader.onload = function(evt) {
        let list = evt.target.result.toString().split('\n')
        for (let i = 0; i <= 12; i++) {
          document.getElementById('row' + (i+1)).value = list[i]
        }
      }
    }
    reader.readAsText(file);
  }
  setTimeout(() => { importfile(yeti) }, 80)
}

var importdescriptor = (line) => {
   let file = document.getElementById("filepath").files[0]
   if (file != undefined) {
     let reader = new FileReader();
     document.getElementById('filepath').value = ""
     reader.onload = function(evt) {
        let list = evt.target.result.toString().split('\n')
        document.getElementById('descriptor').value = list[line]
     }
     reader.readAsText(file);
   }
   setTimeout(() => { importdescriptor(line) }, 80)
 }

 var highlightBin = () => {
   for (var i = 1; i <= 7; i++) {
      var binary = document.getElementById('binary' + i).value
      document.getElementById('count' + i).innerHTML = binary.length + ' \\ 256'
      if (binary.length === 256 && document.getElementById('binary' + i).value.replace(/1/g, '').replace(/0/g,'').length === 0) {
        document.getElementById('binary' + i).style.backgroundColor = "rgba(0, 151, 19, 0.4)"
      } else if (binary.length >= 257 || document.getElementById('binary' + i).value.replace(/1/g, '').replace(/0/g,'').length != 0) {
        document.getElementById('binary' + i).style.backgroundColor = "rgba(255, 0, 0, 0.4)"
      } else {
        document.getElementById('binary' + i).style.backgroundColor = ""
      }
   }
   setTimeout(() => {highlightBin()}, 80)
 }


