#!/bin/bash

CheckSig=$(sha256sum --ignore-missing --check SHA256SUMS | grep --count 'bitcoin-.*-x86_64-linux-gnu.tar.gz: OK')
echo "${CheckSig}"

curl -fsSL https://github.com/bitcoin-core/guix.sigs/raw/main/builder-keys/laanwj.gpg | gpg --import -
RSAKey1="9DEAE0DC7063249FB05474681E4AED62986CD25D"
Fingerprint1="71A3 B167 3540 5025 D447 E8F2 7481 0B01 2346 C9A6"
curl -fsSL https://github.com/bitcoin-core/guix.sigs/raw/main/builder-keys/fanquake.gpg | gpg --import -
RSAKey2="CFB16E21C950F67FA95E558F2EEB9F5CC09526C1"
Fingerprint2="E777 299F C265 DD04 7930 70EB 944D 35F9 AC3D B76A"

verifyResult="$(gpg --verify SHA256SUMS.asc 2>&1)"
goodSignatures="$(echo "${verifyResult}" | grep --count 'Good signature')"
goodRSAKeys="$(echo "${verifyResult}" | grep 'using RSA key ' | grep -oE "${RSAKey1}|${RSAKey2}" | wc -l)"
goodFingerprints="$(echo ${verifyResult} | grep 'Primary key fingerprint' | grep -oE "${Fingerprint1}|${Fingerprint2}" | wc -l)"
echo "${verifyResult}"
echo "${goodSignatures}"
echo "${goodRSAKeys}"
echo "${goodFingerprints}"

if [ "${CheckSig}" -eq 1 ] && [ "${goodSignatures}" -ge 2 ] && [ "${goodRSAKeys}" -ge 2 ] && [ "${goodFingerprints}" -ge 2 ]
then
  touch "${HOME}"/yeticold/sigcorrect
fi
