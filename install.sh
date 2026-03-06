#!/bin/bash
set -e

echo "Sinai Trail — installing..."

if ! command -v python3 &> /dev/null; then
    echo "Python 3 not found. I'm a rock. I can't help you."
    exit 1
fi

mkdir -p "$HOME/.sinaitrail"

curl -fsSL https://raw.githubusercontent.com/alm108/SinaiTrail/main/sinai_trail.py -o "$HOME/.sinaitrail/sinai_trail.py"

cat > /usr/local/bin/sinaitrail << 'EOF'
#!/bin/bash
python3 "$HOME/.sinaitrail/sinai_trail.py"
EOF
chmod +x /usr/local/bin/sinaitrail

echo ""
echo "Done. Type 'sinaitrail' to play."
echo "Rock: you're welcome."
