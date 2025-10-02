#!/bin/bash

###############################################################################
# TODO Scanner - Local Testing Script
# 
# This script simulates what the GitHub Action does locally.
# Use it to test your TODO comments before pushing to GitHub.
#
# Usage:
#   ./scripts/scan_todos.sh                 # Scan all files
#   ./scripts/scan_todos.sh src/            # Scan specific directory
#   ./scripts/scan_todos.sh src/main.py     # Scan specific file
#
# Author: GitHub Copilot
# Date: 2025-10-02
###############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Emojis
CHECK="✅"
CROSS="❌"
WARN="⚠️"
INFO="ℹ️"
FIRE="🔥"
HACK="⚡"
BUG="🐛"
NOTE="📝"

# Configuration
SEARCH_PATH="${1:-.}"
EXCLUDE_DIRS="node_modules|dist|build|__pycache__|.git|opa-wasm-env|.venv|venv"
TODO_TYPES=("TODO" "FIXME" "HACK" "XXX" "BUG" "NOTE")

# Counters
declare -A counts
for type in "${TODO_TYPES[@]}"; do
    counts[$type]=0
done

# Output file
OUTPUT_FILE=".github/TODO_SCAN_RESULT.md"

echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        TODO Scanner - Local Testing Tool                ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to get emoji for type
get_emoji() {
    case $1 in
        TODO) echo "📝" ;;
        FIXME) echo "🔥" ;;
        HACK) echo "⚠️" ;;
        XXX) echo "❗" ;;
        BUG) echo "🐛" ;;
        NOTE) echo "📄" ;;
        *) echo "📌" ;;
    esac
}

# Function to get priority for type
get_priority() {
    case $1 in
        TODO) echo "MEDIUM" ;;
        FIXME) echo "HIGH" ;;
        HACK) echo "MEDIUM" ;;
        XXX) echo "HIGH" ;;
        BUG) echo "CRITICAL" ;;
        NOTE) echo "LOW" ;;
        *) echo "MEDIUM" ;;
    esac
}

# Function to get color for priority
get_priority_color() {
    case $1 in
        CRITICAL) echo "$RED" ;;
        HIGH) echo "$YELLOW" ;;
        MEDIUM) echo "$BLUE" ;;
        LOW) echo "$CYAN" ;;
        *) echo "$NC" ;;
    esac
}

echo -e "${CYAN}${INFO} Scanning path: ${SEARCH_PATH}${NC}"
echo -e "${CYAN}${INFO} Excluding: ${EXCLUDE_DIRS}${NC}"
echo ""

# Create output file
cat > "$OUTPUT_FILE" << 'EOF'
# 🔍 TODO Scan Results

**Scanned:** `date`
**Path:** `SEARCH_PATH`

---

EOF

# Find all TODO comments
echo -e "${GREEN}${CHECK} Scanning for TODO comments...${NC}"
echo ""

# Store results in temporary file
TEMP_FILE=$(mktemp)

# Search for each type
for type in "${TODO_TYPES[@]}"; do
    emoji=$(get_emoji "$type")
    priority=$(get_priority "$type")
    priority_color=$(get_priority_color "$priority")
    
    # Search for pattern: # TODO: or // TODO: or /* TODO: */
    results=$(grep -rn --exclude-dir={${EXCLUDE_DIRS}} \
              -E "(#|//|/\*)\s*${type}:\s*.+" \
              "$SEARCH_PATH" 2>/dev/null || true)
    
    if [ -n "$results" ]; then
        count=$(echo "$results" | wc -l)
        counts[$type]=$count
        
        echo -e "${priority_color}${emoji} Found ${count} ${type} comment(s)${NC}"
        
        # Write to output file
        echo "" >> "$OUTPUT_FILE"
        echo "## ${emoji} ${type} Comments (${count})" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        echo "**Priority:** ${priority}" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        
        # Parse and format results
        echo "$results" | while IFS= read -r line; do
            file=$(echo "$line" | cut -d: -f1)
            line_num=$(echo "$line" | cut -d: -f2)
            comment=$(echo "$line" | cut -d: -f3- | sed 's/^[[:space:]]*//')
            
            # Extract just the comment text (remove markers)
            comment_text=$(echo "$comment" | sed -E 's/(#|\/\/|\/\*)\s*'$type':\s*//')
            
            # Display in console
            echo -e "  ${CYAN}${file}:${line_num}${NC}"
            echo -e "  ${PURPLE}→ ${comment_text}${NC}"
            echo ""
            
            # Write to markdown
            echo "### \`${file}:${line_num}\`" >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
            echo "${comment_text}" >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
            echo '```' >> "$OUTPUT_FILE"
            
            # Get context (3 lines before and after)
            sed -n "$((line_num-2)),$((line_num+2))p" "$file" 2>/dev/null | \
                sed "${line_num}s/^/→ /" >> "$OUTPUT_FILE" 2>/dev/null || true
            
            echo '```' >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
        done
        
        echo "$results" >> "$TEMP_FILE"
    else
        echo -e "${GREEN}${CHECK} No ${type} comments found${NC}"
    fi
done

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""

# Summary
total=0
for type in "${TODO_TYPES[@]}"; do
    total=$((total + counts[$type]))
done

echo -e "${YELLOW}📊 Summary:${NC}"
echo -e "${YELLOW}───────────${NC}"

if [ $total -eq 0 ]; then
    echo -e "${GREEN}${CHECK} No TODO comments found - Great job!${NC}"
else
    for type in "${TODO_TYPES[@]}"; do
        if [ ${counts[$type]} -gt 0 ]; then
            emoji=$(get_emoji "$type")
            priority=$(get_priority "$type")
            priority_color=$(get_priority_color "$priority")
            echo -e "${priority_color}${emoji} ${type}: ${counts[$type]} (${priority})${NC}"
        fi
    done
    
    echo ""
    echo -e "${YELLOW}Total: ${total} comment(s)${NC}"
fi

# Write summary to output file
cat >> "$OUTPUT_FILE" << EOF

---

## 📊 Summary

| Type | Count | Priority |
|------|-------|----------|
EOF

for type in "${TODO_TYPES[@]}"; do
    if [ ${counts[$type]} -gt 0 ]; then
        emoji=$(get_emoji "$type")
        priority=$(get_priority "$type")
        echo "| ${emoji} ${type} | ${counts[$type]} | ${priority} |" >> "$OUTPUT_FILE"
    fi
done

echo "" >> "$OUTPUT_FILE"
echo "**Total:** ${total} TODO comments" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Recommendations
cat >> "$OUTPUT_FILE" << 'EOF'

---

## 💡 Recommendations

EOF

if [ $total -eq 0 ]; then
    echo "🎉 **Excellent!** No TODO comments found. Your code is clean!" >> "$OUTPUT_FILE"
elif [ ${counts[BUG]} -gt 0 ] || [ ${counts[FIXME]} -gt 0 ]; then
    echo "⚠️ **Action Required:** You have critical/high priority items that need attention." >> "$OUTPUT_FILE"
elif [ $total -gt 20 ]; then
    echo "📊 **Consider:** You have many TODO items. Prioritize and tackle them systematically." >> "$OUTPUT_FILE"
else
    echo "✅ **Good:** Manageable number of TODO items. Keep tracking and resolving them." >> "$OUTPUT_FILE"
fi

echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "*Generated by TODO Scanner - $(date)*" >> "$OUTPUT_FILE"

echo ""
echo -e "${GREEN}${CHECK} Results saved to: ${OUTPUT_FILE}${NC}"
echo ""

# Recommendations
if [ $total -gt 0 ]; then
    echo -e "${YELLOW}💡 Next Steps:${NC}"
    echo -e "${YELLOW}─────────────${NC}"
    
    if [ ${counts[BUG]} -gt 0 ]; then
        echo -e "${RED}1. ${FIRE} Fix ${counts[BUG]} BUG comment(s) immediately (CRITICAL)${NC}"
    fi
    
    if [ ${counts[FIXME]} -gt 0 ]; then
        echo -e "${YELLOW}2. ${FIRE} Address ${counts[FIXME]} FIXME comment(s) (HIGH priority)${NC}"
    fi
    
    if [ ${counts[HACK]} -gt 0 ]; then
        echo -e "${BLUE}3. ${HACK} Refactor ${counts[HACK]} HACK comment(s) (Technical debt)${NC}"
    fi
    
    if [ ${counts[TODO]} -gt 0 ]; then
        echo -e "${CYAN}4. ${NOTE} Complete ${counts[TODO]} TODO item(s) (Enhancements)${NC}"
    fi
    
    echo ""
    echo -e "${PURPLE}When you push to GitHub, these will automatically create Issues!${NC}"
fi

echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  To create GitHub Issues, push your changes to main     ║${NC}"
echo -e "${BLUE}║  The workflow will run automatically!                    ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"

# Cleanup
rm -f "$TEMP_FILE"

# Exit with error if critical issues found
if [ ${counts[BUG]} -gt 0 ]; then
    echo ""
    echo -e "${RED}${CROSS} CRITICAL: BUG comments found. Please fix before deploying!${NC}"
    exit 1
fi

exit 0
