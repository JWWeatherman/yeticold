Sig=$(sha256sum --ignore-missing --check SHA256SUMS.asc)
CheckSig=$(echo ${Sig} | grep 'bitcoin-0.21.0-x86_64-linux-gnu.tar.gz: OK' -c)
echo ${CheckSig}
gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys 01EA5486DE18A882D4C2684590C8019E36C2E964

verifyResult=$(gpg --verify SHA256SUMS.asc 2>&1)
goodSignature=$(echo ${verifyResult} | grep 'Good signature' -c)
goodFingerprint=$(echo ${verifyResult} | grep "Primary key fingerprint: 01EA 5486 DE18 A882 D4C2 6845 90C8 019E 36C2 E964" -c)
echo ${verifyResult}
echo ${goodSignature}
echo ${goodFingerprint}

if [ ${CheckSig} -eq 1 ] && [ ${goodSignature} -eq 1 ] && [ ${goodFingerprint} -eq 1 ]
then
  touch ~/yeticold/sigcorrect
fi


