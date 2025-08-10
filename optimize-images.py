#!/usr/bin/env python3
"""
Joy Joe Balloon Twisting - Image Optimization Script (Python)
Creates responsive versions of images for different viewports using PIL
"""

import os
import sys
from PIL import Image
import glob
from pathlib import Path

def create_directories():
    """Create optimized image directories"""
    dirs = [
        'assets/img/optimized/mobile',
        'assets/img/optimized/tablet', 
        'assets/img/optimized/desktop',
        'assets/gallery/optimized/mobile',
        'assets/gallery/optimized/tablet',
        'assets/gallery/optimized/desktop',
        'assets/img/BT/optimized/mobile',
        'assets/img/BT/optimized/tablet',
        'assets/img/BT/optimized/desktop',
        'assets/img/BF/optimized/mobile',
        'assets/img/BF/optimized/tablet', 
        'assets/img/BF/optimized/desktop',
        'assets/img/balloonAnimals/optimized/mobile',
        'assets/img/balloonAnimals/optimized/tablet',
        'assets/img/balloonAnimals/optimized/desktop',
        'assets/img/portfolio/thumbnails/optimized/mobile',
        'assets/img/portfolio/thumbnails/optimized/tablet',
        'assets/img/portfolio/thumbnails/optimized/desktop'
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

def optimize_image(src_path, dest_dir, filename):
    """Optimize a single image for different viewports"""
    try:
        # Open and get original image info
        with Image.open(src_path) as img:
            original_width, original_height = img.size
            original_size = os.path.getsize(src_path)
            
            print(f"🔄 Processing: {filename}")
            print(f"   Original: {original_width}x{original_height} ({original_size//1024}KB)")
            
            # Convert to RGB if necessary (for WebP compatibility)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Define viewport sizes and quality
            sizes = {
                'mobile': {'width': 400, 'quality': 75},
                'tablet': {'width': 768, 'quality': 80}, 
                'desktop': {'width': 1200, 'quality': 85}
            }
            
            name_without_ext = os.path.splitext(filename)[0]
            
            for viewport, config in sizes.items():
                max_width = config['width']
                quality = config['quality']
                
                # Don't upscale images smaller than target width
                if original_width <= max_width:
                    new_width = original_width
                    new_height = original_height
                else:
                    # Calculate new dimensions maintaining aspect ratio
                    ratio = max_width / original_width
                    new_width = max_width
                    new_height = int(original_height * ratio)
                
                # Resize image
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Save as WebP
                output_path = f"{dest_dir}/{viewport}/{name_without_ext}.webp"
                resized_img.save(output_path, 'WebP', quality=quality, optimize=True)
                
                # Get optimized size
                optimized_size = os.path.getsize(output_path)
                savings = ((original_size - optimized_size) / original_size) * 100
                
                print(f"   ✅ {viewport.capitalize()}: {new_width}x{new_height} ({optimized_size//1024}KB, {savings:.1f}% savings)")
                
    except Exception as e:
        print(f"   ❌ Error processing {filename}: {str(e)}")

def main():
    print("🎈 Joy Joe Balloon Twisting - Python Image Optimization")
    print("=" * 56)
    
    # Check if PIL is available
    try:
        from PIL import Image
    except ImportError:
        print("❌ PIL (Pillow) not found. Please install it first:")
        print("   pip3 install Pillow")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    print("\n📱 Creating responsive images:")
    print("   Mobile: 400px (Quality: 75%)")
    print("   Tablet: 768px (Quality: 80%)")
    print("   Desktop: 1200px (Quality: 85%)")
    print()
    
    # Define image collections to optimize
    image_collections = [
        # Main images
        {
            'pattern': 'assets/img/portfolio/thumbnails/logo.png',
            'dest_dir': 'assets/img/portfolio/thumbnails/optimized',
            'description': 'Logo'
        },
        {
            'pattern': 'assets/img/portfolio/thumbnails/g6.webp',
            'dest_dir': 'assets/img/portfolio/thumbnails/optimized',
            'description': 'Hero Image'
        },
        
        # Service images - Balloon Twisting
        {
            'pattern': 'assets/img/BT/*.webp',
            'dest_dir': 'assets/img/BT/optimized',
            'description': 'Balloon Twisting Services'
        },
        
        # Service images - Balloon Flowers
        {
            'pattern': 'assets/img/BF/*.webp',
            'dest_dir': 'assets/img/BF/optimized',
            'description': 'Balloon Flowers'
        },
        
        # Service images - Balloon Characters
        {
            'pattern': 'assets/img/BD*.webp',
            'dest_dir': 'assets/img/optimized',
            'description': 'Balloon Characters'
        },
        
        # Balloon Animals
        {
            'pattern': 'assets/img/balloonAnimals/*.webp',
            'dest_dir': 'assets/img/balloonAnimals/optimized',
            'description': 'Balloon Animals'
        },
        
        # Gallery images
        {
            'pattern': 'assets/gallery/*.webp',
            'dest_dir': 'assets/gallery/optimized',
            'description': 'Gallery Images'
        },
        
        # Other service images
        {
            'pattern': 'assets/img/balloonNumber.webp',
            'dest_dir': 'assets/img/optimized',
            'description': 'Balloon Number'
        },
        {
            'pattern': 'assets/img/candy_cup.webp',
            'dest_dir': 'assets/img/optimized',
            'description': 'Candy Cup'
        },
        
        # About page images
        {
            'pattern': 'assets/img/magicjoe.PNG',
            'dest_dir': 'assets/img/optimized',
            'description': 'Magic Joe Photo'
        },
        {
            'pattern': 'assets/img/magicjoeandpuppet.PNG',
            'dest_dir': 'assets/img/optimized',
            'description': 'Magic Joe with Puppet'
        }
    ]
    
    total_processed = 0
    
    # Process each collection
    for collection in image_collections:
        pattern = collection['pattern']
        dest_dir = collection['dest_dir']
        description = collection['description']
        
        print(f"\n🖼️  Optimizing {description}...")
        print("-" * 40)
        
        # Find matching files
        files = glob.glob(pattern)
        
        if not files:
            print(f"   ⚠️  No files found matching: {pattern}")
            continue
            
        for file_path in files:
            if os.path.isfile(file_path):
                filename = os.path.basename(file_path)
                optimize_image(file_path, dest_dir, filename)
                total_processed += 1
    
    print(f"\n✨ Image Optimization Complete!")
    print("=" * 40)
    print(f"   📊 Total images processed: {total_processed}")
    print(f"   📁 Optimized images saved to */optimized/ directories")
    print(f"   🚀 Expected performance improvement: 2-4 seconds faster loading")
    print(f"   💾 Expected data savings: 60-80% on mobile devices")
    print()
    print("🔗 Next steps:")
    print("   1. Update HTML files to use responsive <picture> elements")
    print("   2. Test loading performance across different devices")
    print("   3. Monitor PageSpeed Insights for improvements")

if __name__ == "__main__":
    main()
