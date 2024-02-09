#!/bin/bash

check_sig=$(sha256sum --ignore-missing --check SHA256SUMS | grep --count 'bitcoin-.*-x86_64-linux-gnu.tar.gz: OK')
echo "${check_sig}"

if [ "${check_sig}" -eq 1 ]; then
  curl -fsSL https://github.com/bitcoin-core/guix.sigs/raw/main/builder-keys/laanwj.gpg | gpg --import -
  rsa_key_1="9DEAE0DC7063249FB05474681E4AED62986CD25D"
  fingerprint_1="71A3 B167 3540 5025 D447 E8F2 7481 0B01 2346 C9A6"
  curl -fsSL https://github.com/bitcoin-core/guix.sigs/raw/main/builder-keys/fanquake.gpg | gpg --import -
  rsa_key_2="CFB16E21C950F67FA95E558F2EEB9F5CC09526C1"
  fingerprint_2="E777 299F C265 DD04 7930 70EB 944D 35F9 AC3D B76A"
  curl -fsSL https://github.com/bitcoin-core/guix.sigs/raw/main/builder-keys/Sjors.gpg | gpg --import -
  rsa_key_3="ED9BDF7AD6A55E232E84524257FF9BDBCC301009"
  fingerprint_3="ED9B DF7A D6A5 5E23 2E84 5242 57FF 9BDB CC30 1009"
  curl -fsSL https://github.com/bitcoin-core/guix.sigs/raw/main/builder-keys/achow101.gpg | gpg --import -
  rsa_key_4="152812300785C96444D3334D17565732E08E5E41"
  fingerprint_4="1528 1230 0785 C964 44D3 334D 1756 5732 E08E 5E41"

  verify_result="$(gpg --verify SHA256SUMS.asc 2>&1)"
  good_signatures="$(echo "${verify_result}" | grep --count 'Good signature')"
  good_rsa_keys="$(echo "${verify_result}" | grep 'using RSA key ' | grep -oE "${rsa_key_1}|${rsa_key_2}|${rsa_key_3}|${rsa_key_4}" | wc -l)"
  good_fingerprints="$(echo ${verify_result} | grep 'Primary key fingerprint' | grep -oE "${fingerprint_1}|${fingerprint_2}|${fingerprint_3}|${fingerprint_4}" | wc -l)"
  echo "${verify_result}"
  echo "${good_signatures}"
  echo "${good_rsa_keys}"
  echo "${good_fingerprints}"

  reqd_sigs="4"
  if [ "${good_signatures}" -ge "${reqd_sigs}" ] && [ "${good_rsa_keys}" -ge "${reqd_sigs}" ] && [ "${good_fingerprints}" -ge "${reqd_sigs}" ]; then
    touch "${HOME}"/yeticold/sigcorrect
  fi
fi
