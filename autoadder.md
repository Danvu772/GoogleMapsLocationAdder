# Google maps travel list auto adder
I quickly created a script to automatically traverse through google maps and automatically add locations to the travel list in google maps. After it puts all of your locations into your travel plans list, you can automatically add them into your own lists. 

## Implementing the Google Maps Auto-add Script with a Logged-in Browser Profile

Using a browser profile where you're already logged into Google Maps can bypass the login process and make the script more reliable. Here's a complete guide:

## Step 1: Set up your virtual environment

```bash
# Create a virtual environment
python -m venv maps_env

# Activate the virtual environment
# On Windows:
maps_env\Scripts\activate
# On macOS/Linux:
source maps_env/bin/activate
```

## Step 2: Install required packages

```bash
pip install selenium webdriver-manager
```

## Step 3: Find your Chrome profile directory

### For Windows:
1. Open Chrome
2. Type `chrome://version` in the address bar
3. Look for "Profile Path" - it will show your profile directory
4. The `user_data_dir` is the path up to (but not including) the "Profile" directory

### For macOS:
1. Open Chrome
2. Type `chrome://version` in the address bar
3. Look for "Profile Path"
4. The `user_data_dir` is typically `/Users/YourUsername/Library/Application Support/Google/Chrome`

### For Linux:
1. Open Chrome
2. Type `chrome://version` in the address bar
3. Look for "Profile Path"
4. The `user_data_dir` is typically `/home/YourUsername/.config/google-chrome`

## Step 4: Update the script with your profile information

Edit the `user_data_dir` and `profile_directory` variables in the script with the values you found in Step 4.

## Step 5: Create your travel list in Google Maps

Before running the script:
- In the script, update your places_list to include google queryable search terms for the places that you would like to visit. (the more specific and queryable the better) 

After running the script:
- In Google Maps, the places that you've added to travel list will automatically sort into locations. Create a new list from this auto-generated list or customize it any way you want!


## Step 6: Run the script

With your virtual environment activated:

```bash
python google_maps_adder.py
```

## Troubleshooting Tips:

1. **Browser closing immediately**: Increase the `time.sleep()` values to give yourself more time to see what's happening.

2. **XPath selector issues**: If the script can't find elements, the Google Maps interface might have changed. Try opening the browser DevTools (F12), and use the inspector to find the new selectors.

3. **Permission errors accessing profile**: Make sure Chrome is completely closed before running the script.

4. **"user-data-dir" errors**: Double-check your profile path and make sure it's properly escaped if there are spaces.

5. **Google detecting automation**: Add the following argument to make detection harder:
   ```python
   chrome_options.add_argument("--disable-blink-features=AutomationControlled")
   ```

6. **Profile locked errors**: This means Chrome is already using that profile. Close all Chrome instances first.

7. **Different UI issues**: Adjust the XPath selectors based on what you see in your browser. The Google Maps interface can vary by region and account.

Remember that using your profile means the script needs your Chrome profile to be logged into Google. If you log out of Google in Chrome, the script will also be logged out.