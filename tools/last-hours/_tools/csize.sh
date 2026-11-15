# sizes of the biggest places on C: (one line per folder as it finishes)
for d in "C:/Users/ossam/AppData/Local/"*/ "C:/Users/ossam/AppData/Roaming" "C:/Users/ossam/Downloads" "C:/Users/ossam/Documents" "C:/Users/ossam/Desktop" "C:/Users/ossam/.cache" "C:/Users/ossam/.docker" "C:/ProgramData" "C:/Program Files" "C:/Program Files (x86)" "C:/Windows"; do
  printf "%s\t%s\n" "$(du -sm "$d" 2>/dev/null | cut -f1)" "$d"
done
