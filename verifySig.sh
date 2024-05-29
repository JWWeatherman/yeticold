#!/bin/bash

readonly CHECK_SIG=$(sha256sum --ignore-missing --check SHA256SUMS | grep --count 'bitcoin-.*-x86_64-linux-gnu.tar.gz: OK')
echo "${CHECK_SIG}"

if [ "${CHECK_SIG}" -eq 1 ]; then
  curl -fsSL https://github.com/bitcoin-core/guix.sigs/raw/main/builder-keys/laanwj.gpg | gpg --import -
  readonly RSA_KEY_1="9DEAE0DC7063249FB05474681E4AED62986CD25D"
  readonly FINGERPRINT_1="71A3 B167 3540 5025 D447 E8F2 7481 0B01 2346 C9A6"
  curl -fsSL https://github.com/bitcoin-core/guix.sigs/raw/main/builder-keys/fanquake.gpg | gpg --import -
  readonly RSA_KEY_2="CFB16E21C950F67FA95E558F2EEB9F5CC09526C1"
  readonly FINGERPRINT_2="E777 299F C265 DD04 7930 70EB 944D 35F9 AC3D B76A"
  curl -fsSL https://github.com/bitcoin-core/guix.sigs/raw/main/builder-keys/Sjors.gpg | gpg --import -
  readonly RSA_KEY_3="ED9BDF7AD6A55E232E84524257FF9BDBCC301009"
  readonly FINGERPRINT_3="ED9B DF7A D6A5 5E23 2E84 5242 57FF 9BDB CC30 1009"
  curl -fsSL https://github.com/bitcoin-core/guix.sigs/raw/main/builder-keys/achow101.gpg | gpg --import -
  readonly RSA_KEY_4="152812300785C96444D3334D17565732E08E5E41"
  readonly FINGERPRINT_4="1528 1230 0785 C964 44D3 334D 1756 5732 E08E 5E41"

  readonly VERIFY_RESULT="$(gpg --verify SHA256SUMS.asc 2>&1)"
  readonly GOOD_SIGNATURES="$(echo "${VERIFY_RESULT}" | grep --count 'Good signature')"
  readonly GOOD_RSA_KEYS="$(echo "${VERIFY_RESULT}" | grep 'using RSA key ' | grep -oE "${RSA_KEY_1}|${RSA_KEY_2}|${RSA_KEY_3}|${RSA_KEY_4}" | wc -l)"
  readonly GOOD_FINGERPRINTS="$(echo ${VERIFY_RESULT} | grep 'Primary key fingerprint' | grep -oE "${FINGERPRINT_1}|${FINGERPRINT_2}|${FINGERPRINT_3}|${FINGERPRINT_4}" | wc -l)"
  echo "${VERIFY_RESULT}"
  echo "${GOOD_SIGNATURES}"
  echo "${GOOD_RSA_KEYS}"
  echo "${GOOD_FINGERPRINTS}"

  readonly REQD_SIGS="4"
  if [ "${GOOD_SIGNATURES}" -ge "${REQD_SIGS}" ] && [ "${GOOD_RSA_KEYS}" -ge "${REQD_SIGS}" ] && [ "${GOOD_FINGERPRINTS}" -ge "${REQD_SIGS}" ]; then
    touch "${HOME}/yeticold/sigcorrect"
  fi
fi
