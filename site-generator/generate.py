import os
import json
import shutil

def build_dist():
    # Define directories
    dist_dir = 'dist'
    
    # 1. Clean or create dist directory
    os.makedirs(dist_dir, exist_ok=True)
    
    # 2. Copy generic root landing index.html to dist/
    if os.path.exists('index.html'):
        shutil.copy('index.html', os.path.join(dist_dir, 'index.html'))
        print("Copied generic root landing page to dist/")
    # Copy .htaccess to dist/ if it exists (for Apache server routing redirects)
    htaccess_src = '../.htaccess'
    if not os.path.exists(htaccess_src):
        htaccess_src = '.htaccess'
        
    if os.path.exists(htaccess_src):
        shutil.copy(htaccess_src, os.path.join(dist_dir, '.htaccess'))
        print("Copied .htaccess file to dist/ for server routing")
    else:
        print("Warning: .htaccess file not found!")

    # Copy assets/ folder if it exists (for uploaded custom OG images)
    if os.path.exists('assets'):
        shutil.copytree('assets', os.path.join(dist_dir, 'assets'), dirs_exist_ok=True)
        print("Copied custom upload assets to dist/assets/")
    # 3. Load vendor config
    if not os.path.exists('vendors.json'):
        print("Error: vendors.json not found!")
        return
    with open('vendors.json', 'r', encoding='utf-8') as f:
        vendors = json.load(f)

    # 4. Load template
    if not os.path.exists('template.html'):
        print("Error: template.html not found!")
        return
    with open('template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    print(f"Loaded {len(vendors)} vendor configurations.")

    # 5. Compile each vendor site into dist/
    for vendor in vendors:
        # Skip compilation for disabled/inactive clients
        if not vendor.get('active', True):
            print(f"Skipping inactive client: {vendor.get('locationName')} ({vendor.get('locationId')})")
            continue
            
        loc_id = vendor['locationId']
        short_id = vendor.get('shortId', '')
        name = vendor['locationName']
        place_id = vendor['placeId']
        ga_id = vendor.get('googleAnalyticsId', '')
        og_title = vendor.get('ogTitle', f"Review {name} on Buzl")
        og_desc = vendor.get('ogDescription', f"Draft an honest Google review for {name} using our interactive assistant.")
        og_img = vendor.get('ogImage', 'https://gobuzl.com/assets/og-image-default.png')

        # Replace placeholders in template
        html = template
        html = html.replace('{{LOCATION_ID}}', loc_id)
        html = html.replace('{{SHORT_ID}}', short_id)
        html = html.replace('{{LOCATION_NAME}}', name)
        html = html.replace('{{PLACE_ID}}', place_id)
        html = html.replace('{{GOOGLE_ANALYTICS_ID}}', ga_id)
        html = html.replace('{{OG_TITLE}}', og_title)
        html = html.replace('{{OG_DESCRIPTION}}', og_desc)
        html = html.replace('{{OG_IMAGE}}', og_img)

        # Output to folders matching the location IDs (for clean URL routing)
        paths_to_create = [loc_id]
        if short_id:
            paths_to_create.append(short_id)

        for path_segment in paths_to_create:
            target_path = os.path.join(dist_dir, path_segment)
            os.makedirs(target_path, exist_ok=True)
            output_file = os.path.join(target_path, 'index.html')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f" -> Generated static site at: /dist/{path_segment}/index.html")

    print("\nStatic site build completed! Deployed content is ready in the /dist/ directory.")

if __name__ == '__main__':
    build_dist()
