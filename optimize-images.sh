#!/bin/bash

# Image Optimization Script for Joy Joe Balloon Twisting Website
# This script creates responsive versions of images for different viewports

echo "🎈 Joy Joe Balloon Twisting - Image Optimization Script"
echo "======================================================"

# Check if imagemagick is installed
if ! command -v magick &> /dev/null && ! command -v convert &> /dev/null; then
    echo "❌ ImageMagick not found. Please install it first:"
    echo "   macOS: brew install imagemagick"
    echo "   Ubuntu: sudo apt-get install imagemagick"
    echo "   Windows: Download from https://imagemagick.org/"
    exit 1
fi

# Use 'magick' if available (ImageMagick 7), otherwise 'convert' (ImageMagick 6)
if command -v magick &> /dev/null; then
    CONVERT="magick"
else
    CONVERT="convert"
fi

# Create optimized directories
mkdir -p assets/img/optimized/{mobile,tablet,desktop}
mkdir -p assets/gallery/optimized/{mobile,tablet,desktop}
mkdir -p assets/img/BT/optimized/{mobile,tablet,desktop}
mkdir -p assets/img/BF/optimized/{mobile,tablet,desktop}
mkdir -p assets/img/balloonAnimals/optimized/{mobile,tablet,desktop}
mkdir -p assets/img/portfolio/thumbnails/optimized/{mobile,tablet,desktop}

# Define viewport sizes
MOBILE_WIDTH=400
TABLET_WIDTH=768  
DESKTOP_WIDTH=1200

# Quality settings
MOBILE_QUALITY=75
TABLET_QUALITY=80
DESKTOP_QUALITY=85

echo ""
echo "📱 Viewport Sizes:"
echo "   Mobile: ${MOBILE_WIDTH}px (Quality: ${MOBILE_QUALITY}%)"
echo "   Tablet: ${TABLET_WIDTH}px (Quality: ${TABLET_QUALITY}%)"
echo "   Desktop: ${DESKTOP_WIDTH}px (Quality: ${DESKTOP_QUALITY}%)"
echo ""

# Function to optimize images
optimize_image() {
    local src_file="$1"
    local dest_dir="$2"
    local filename=$(basename "$src_file")
    local name_without_ext="${filename%.*}"
    local ext="${filename##*.}"
    
    if [[ ! -f "$src_file" ]]; then
        echo "⚠️  Source file not found: $src_file"
        return
    fi
    
    echo "🔄 Processing: $filename"
    
    # Get original dimensions
    local original_info=$($CONVERT "$src_file" -ping -format "%wx%h" info:)
    local original_width=$(echo $original_info | cut -d'x' -f1)
    local original_height=$(echo $original_info | cut -d'x' -f2)
    
    echo "   Original: ${original_width}x${original_height}"
    
    # Mobile version (400px max width)
    local mobile_width=$MOBILE_WIDTH
    if [[ $original_width -lt $mobile_width ]]; then
        mobile_width=$original_width
    fi
    
    $CONVERT "$src_file" \
        -resize "${mobile_width}x>" \
        -quality $MOBILE_QUALITY \
        -strip \
        "$dest_dir/mobile/${name_without_ext}.webp"
    
    # Tablet version (768px max width)
    local tablet_width=$TABLET_WIDTH
    if [[ $original_width -lt $tablet_width ]]; then
        tablet_width=$original_width
    fi
    
    $CONVERT "$src_file" \
        -resize "${tablet_width}x>" \
        -quality $TABLET_QUALITY \
        -strip \
        "$dest_dir/tablet/${name_without_ext}.webp"
    
    # Desktop version (1200px max width)
    local desktop_width=$DESKTOP_WIDTH
    if [[ $original_width -lt $desktop_width ]]; then
        desktop_width=$original_width
    fi
    
    $CONVERT "$src_file" \
        -resize "${desktop_width}x>" \
        -quality $DESKTOP_QUALITY \
        -strip \
        "$dest_dir/desktop/${name_without_ext}.webp"
    
    # Get optimized sizes
    local mobile_size=$(du -h "$dest_dir/mobile/${name_without_ext}.webp" | cut -f1)
    local tablet_size=$(du -h "$dest_dir/tablet/${name_without_ext}.webp" | cut -f1)
    local desktop_size=$(du -h "$dest_dir/desktop/${name_without_ext}.webp" | cut -f1)
    
    echo "   ✅ Mobile: ${mobile_size} | Tablet: ${tablet_size} | Desktop: ${desktop_size}"
}

# Optimize main images
echo "🖼️  Optimizing Main Images..."
echo "================================"

# Hero background image
if [[ -f "assets/img/bg-masthead.jpg" ]]; then
    optimize_image "assets/img/bg-masthead.jpg" "assets/img/optimized"
fi

# Logo
if [[ -f "assets/img/portfolio/thumbnails/logo.png" ]]; then
    optimize_image "assets/img/portfolio/thumbnails/logo.png" "assets/img/portfolio/thumbnails/optimized"
fi

# Main portfolio image
if [[ -f "assets/img/portfolio/thumbnails/g6.webp" ]]; then
    optimize_image "assets/img/portfolio/thumbnails/g6.webp" "assets/img/portfolio/thumbnails/optimized"
fi

# Service images
echo ""
echo "🎈 Optimizing Service Images..."
echo "==============================="

# Balloon Twisting (BT) images
for img in assets/img/BT/*.webp; do
    if [[ -f "$img" ]]; then
        optimize_image "$img" "assets/img/BT/optimized"
    fi
done

# Balloon Flowers (BF) images  
for img in assets/img/BF/*.webp; do
    if [[ -f "$img" ]]; then
        optimize_image "$img" "assets/img/BF/optimized"
    fi
done

# Balloon Characters (BD) images
for img in assets/img/BD*.webp; do
    if [[ -f "$img" ]]; then
        optimize_image "$img" "assets/img/optimized"
    fi
done

# Balloon Animals
for img in assets/img/balloonAnimals/*.webp; do
    if [[ -f "$img" ]]; then
        optimize_image "$img" "assets/img/balloonAnimals/optimized"
    fi
done

# Other service images
if [[ -f "assets/img/balloonNumber.webp" ]]; then
    optimize_image "assets/img/balloonNumber.webp" "assets/img/optimized"
fi

if [[ -f "assets/img/candy_cup.webp" ]]; then
    optimize_image "assets/img/candy_cup.webp" "assets/img/optimized"
fi

# About page images
if [[ -f "assets/img/magicjoe.PNG" ]]; then
    optimize_image "assets/img/magicjoe.PNG" "assets/img/optimized"
fi

if [[ -f "assets/img/magicjoeandpuppet.PNG" ]]; then
    optimize_image "assets/img/magicjoeandpuppet.PNG" "assets/img/optimized"
fi

# Gallery images
echo ""
echo "🎪 Optimizing Gallery Images..."
echo "==============================="

for img in assets/gallery/*.webp; do
    if [[ -f "$img" ]]; then
        optimize_image "$img" "assets/gallery/optimized"
    fi
done

# Menu images
echo ""
echo "📋 Optimizing Menu Images..."
echo "============================"

if [[ -f "assets/menu/1.png" ]]; then
    optimize_image "assets/menu/1.png" "assets/img/optimized"
fi

if [[ -f "assets/menu/2.png" ]]; then
    optimize_image "assets/menu/2.png" "assets/img/optimized"
fi

echo ""
echo "✨ Image Optimization Complete!"
echo "=============================="
echo ""
echo "📊 Summary:"
echo "   • Created responsive versions for mobile (400px), tablet (768px), desktop (1200px)"
echo "   • Converted all images to WebP format for better compression"
echo "   • Applied progressive quality settings (75%-85%)"
echo "   • Stripped metadata to reduce file sizes"
echo ""
echo "📁 Optimized images are located in:"
echo "   • assets/img/optimized/{mobile,tablet,desktop}/"
echo "   • assets/gallery/optimized/{mobile,tablet,desktop}/"
echo "   • assets/img/BT/optimized/{mobile,tablet,desktop}/"
echo "   • assets/img/BF/optimized/{mobile,tablet,desktop}/"
echo "   • assets/img/balloonAnimals/optimized/{mobile,tablet,desktop}/"
echo ""
echo "🚀 Next steps:"
echo "   1. Update HTML files to use responsive images with <picture> elements"
echo "   2. Test loading performance across different devices"
echo "   3. Monitor PageSpeed Insights for improvements"
echo ""
