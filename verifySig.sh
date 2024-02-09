#!/bin/bash

CheckSig=$(sha256sum --ignore-missing --check SHA256SUMS | grep --count 'bitcoin-.*-x86_64-linux-gnu.tar.gz: OK')
echo "${CheckSig}"

curl -fsSL https://github.com/bitcoin-core/guix.sigs/raw/main/builder-keys/laanwj.gpg | gpg --import -
RSAKey1="9DEAE0DC7063249FB05474681E4AED62986CD25D"
Fingerprint1="71A3 B167 3540 5025 D447 E8F2 7481 0B01 2346 C9A6"
curl -fsSL https://github.com/bitcoin-core/guix.sigs/raw/main/builder-keys/fanquake.gpg | gpg --import -
RSAKey2="CFB16E21C950F67FA95E558F2EEB9F5CC09526C1"
Fingerprint2="E777 299F C265 DD04 7930 70EB 944D 35F9 AC3D B76A"
curl -fsSL https://github.com/bitcoin-core/guix.sigs/raw/main/builder-keys/Sjors.gpg | gpg --import -
RSAKey3="ED9BDF7AD6A55E232E84524257FF9BDBCC301009"
Fingerprint3="ED9B DF7A D6A5 5E23 2E84 5242 57FF 9BDB CC30 1009"
curl -fsSL https://github.com/bitcoin-core/guix.sigs/raw/main/builder-keys/achow101.gpg | gpg --import -
RSAKey4="152812300785C96444D3334D17565732E08E5E41"
Fingerprint4="1528 1230 0785 C964 44D3 334D 1756 5732 E08E 5E41"

verifyResult="$(gpg --verify SHA256SUMS.asc 2>&1)"
goodSignatures="$(echo "${verifyResult}" | grep --count 'Good signature')"
goodRSAKeys="$(echo "${verifyResult}" | grep 'using RSA key ' | grep -oE "${RSAKey1}|${RSAKey2}|${RSAKey3}|${RSAKey4}" | wc -l)"
goodFingerprints="$(echo ${verifyResult} | grep 'Primary key fingerprint' | grep -oE "${Fingerprint1}|${Fingerprint2}|${Fingerprint3}|${Fingerprint4}" | wc -l)"
echo "${verifyResult}"
echo "${goodSignatures}"
echo "${goodRSAKeys}"
echo "${goodFingerprints}"

if [ "${CheckSig}" -eq 1 ] && [ "${goodSignatures}" -ge 4 ] && [ "${goodRSAKeys}" -ge 4 ] && [ "${goodFingerprints}" -ge 4 ]
then
  touch "${HOME}"/yeticold/sigcorrect
fi
