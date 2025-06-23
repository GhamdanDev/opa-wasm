#!/bin/bash

POLICY_PATH="example.rego"
OUTPUT_DIR="."
ENTRYPOINT="authz/allow"

echo "🧹 Removing old artifacts..."
rm -rf $OUTPUT_DIR/bundle.tar.gz $OUTPUT_DIR/bundle $OUTPUT_DIR/policy.wasm $OUTPUT_DIR/data.json

echo "🔨 Building OPA policy bundle..."
opa build -t wasm -e $ENTRYPOINT $POLICY_PATH

if [ -f bundle.tar.gz ]; then
    echo "📦 Extracting WASM file..."
    mkdir -p $OUTPUT_DIR/bundle
    tar -xzf bundle.tar.gz -C $OUTPUT_DIR/bundle
    mv $OUTPUT_DIR/bundle/policy.wasm $OUTPUT_DIR/policy.wasm
    echo "{}" > $OUTPUT_DIR/data.json
else
    echo "❌ bundle.tar.gz not found. Build failed."
    exit 1
fi

if file $OUTPUT_DIR/policy.wasm | grep -q "WebAssembly"; then
    echo "✅ OPA WASM policy built successfully at $OUTPUT_DIR/policy.wasm"
else
    echo "❌ Failed to build valid WASM policy"
fi
