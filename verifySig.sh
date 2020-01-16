Sig=$(sha256sum --ignore-missing --check SHA256SUMS.asc)
CheckSig=$(echo ${Sig} | grep 'bitcoin-0.19.0.1-x86_64-linux-gnu.tar.gz: OK' -c)
echo ${CheckSig}
gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys 01EA5486DE18A882D4C2684590C8019E36C2E964

verifyResult=$(gpg --verify SHA256SUMS.asc 2>&1)
goodSignature=$(echo ${verifyResult} | grep 'Good signature' -c)

if [ ${CheckSig} -eq 1 ] && [ ${goodSignature} -eq 1 ]
then
  touch ~/yeticold/sigcorrect
fi


