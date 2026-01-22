# Video Button & Emoji Removal Plan

## Issues Identified

### 1. Video Not Playing on crmA Page
**File**: [`lichen_crma.html`](../lichen_crma.html:352)

**Current Implementation**:
- Video button exists at line 314-316
- Video modal dialog exists at lines 343-364
- Video element at lines 352-356 references:
  - Primary source: `Images/SupVideo1.mov` (QuickTime format)
  - Fallback source: `Images/SupVideo1.mp4` (MP4 format - doesn't exist)

**Root Cause Analysis**:
- The `.mov` file exists at [`Images/SupVideo1.mov`](../Images/SupVideo1.mov)
- The `.mp4` fallback doesn't exist
- Browser compatibility issues with `.mov` format (QuickTime)
- Many modern browsers (especially on non-Apple platforms) don't natively support `.mov` playback

**Solution Options**:
1. **Convert video to MP4** (Recommended): Convert the `.mov` file to `.mp4` format for better cross-browser compatibility
2. **Update video element**: If conversion isn't possible, adjust the video element to handle `.mov` properly with better attributes

### 2. Emojis Not Loading Properly in Deployment

**Problem**: Emojis in buttons are not rendering consistently across different deployment environments and browsers.

**Emoji Locations Found**:

#### A. "Switch Paper" Button (📚) - 13 files
1. [`bgcs.html`](../bgcs.html:139) - Line 139
2. [`cblaster.html`](../cblaster.html:193) - Line 193
3. [`gcf_search.html`](../gcf_search.html:239) - Line 239
4. [`gcfs.html`](../gcfs.html:188) - Line 188
5. [`ImportantCaveats.html`](../ImportantCaveats.html:88) - Line 88
6. [`lichen_crma.html`](../lichen_crma.html:310) - Line 310
7. [`lichen_landing.html`](../lichen_landing.html:210) - Line 210
8. [`lichen_lff1.html`](../lichen_lff1.html:213) - Line 213
9. [`lichen_lff2.html`](../lichen_lff2.html:212) - Line 212
10. [`lichen_lff3.html`](../lichen_lff3.html:212) - Line 212
11. [`lichen_lff4.html`](../lichen_lff4.html:212) - Line 212
12. [`nar_2023_home.html`](../nar_2023_home.html:104) - Line 104
13. [`species_accession.html`](../species_accession.html:239) - Line 239
14. [`taxa_search.html`](../taxa_search.html:244) - Line 244

#### B. "crmA Warning" Button (⚠️) - 6 files
**Button text**:
1. [`cblaster.html`](../cblaster.html:221) - Line 221
2. [`gcf_search.html`](../gcf_search.html:268) - Line 268
3. [`gcfs.html`](../gcfs.html:217) - Line 217
4. [`species_accession.html`](../species_accession.html:268) - Line 268
5. [`taxa_search.html`](../taxa_search.html:273) - Line 273

**Modal header**:
1. [`cblaster.html`](../cblaster.html:229) - Line 229
2. [`gcf_search.html`](../gcf_search.html:276) - Line 276
3. [`gcfs.html`](../gcfs.html:225) - Line 225
4. [`species_accession.html`](../species_accession.html:276) - Line 276
5. [`taxa_search.html`](../taxa_search.html:281) - Line 281

#### C. "Supplemental Video" Button (🎬) - 1 file
1. [`lichen_crma.html`](../lichen_crma.html:315) - Line 315

#### D. "crmA Species Table" Accordion (📋) - 1 file
1. [`lichen_crma.html`](../lichen_crma.html:394) - Line 394

#### E. Download Buttons (⬇️) - 4 files
1. [`lichen_lff1.html`](../lichen_lff1.html:254) - Line 254
2. [`lichen_lff2.html`](../lichen_lff2.html:253) - Line 253
3. [`lichen_lff3.html`](../lichen_lff3.html:253) - Line 253
4. [`lichen_lff4.html`](../lichen_lff4.html:253) - Line 253

## Implementation Plan

### Phase 1: Fix Video Playback Issue

**Step 1a**: Convert video to MP4 format (if tools available)
- Use `ffmpeg` or similar tool to convert `Images/SupVideo1.mov` to `Images/SupVideo1.mp4`
- Command: `ffmpeg -i Images/SupVideo1.mov -codec:v libx264 -codec:a aac -strict experimental Images/SupVideo1.mp4`

**Step 1b**: Verify video element configuration
- Update [`lichen_crma.html`](../lichen_crma.html:352) video element if needed
- Ensure both source formats are properly listed
- Add additional attributes for better playback: `preload="metadata"` or `controlsList` if needed

### Phase 2: Remove All Emojis from Buttons

**Group A - "Switch Paper" Buttons (14 files)**:
Replace: `📚 Switch Paper` → `Switch Paper`

**Group B - "crmA Warning" Buttons (5 files)**:
Replace: `⚠️ CLICK HERE IF LOOKING INTO crmA` → `CLICK HERE IF LOOKING INTO crmA`
Replace: `⚠️ Important Update on crmA Data` → `Important Update on crmA Data`

**Group C - "Supplemental Video" Button (1 file)**:
Replace: `🎬 Supplemental Video` → `Supplemental Video`

**Group D - "crmA Species Table" Accordion (1 file)**:
Replace: `📋 crmA Species Table (Click to expand)` → `crmA Species Table (Click to expand)`

**Group E - Download Buttons (4 files)**:
Replace: `⬇️ Download GBK Files` → `Download GBK Files`

### Phase 3: Testing

1. **Test video playback**:
   - Open [`lichen_crma.html`](../lichen_crma.html) in browser
   - Click "Supplemental Video" button
   - Verify video plays in modal
   - Test on multiple browsers (Chrome, Firefox, Safari, Edge)

2. **Verify emoji removal**:
   - Visually inspect all buttons on all pages
   - Confirm text is clear and buttons are functional
   - Check deployment to ensure proper rendering

## Files to Modify

### High Priority (Video Issue)
1. [`lichen_crma.html`](../lichen_crma.html) - Fix video playback
2. Create `Images/SupVideo1.mp4` if possible

### Emoji Removal (24 files, ~34 replacements)
1. [`bgcs.html`](../bgcs.html)
2. [`cblaster.html`](../cblaster.html)
3. [`gcf_search.html`](../gcf_search.html)
4. [`gcfs.html`](../gcfs.html)
5. [`ImportantCaveats.html`](../ImportantCaveats.html)
6. [`lichen_crma.html`](../lichen_crma.html)
7. [`lichen_landing.html`](../lichen_landing.html)
8. [`lichen_lff1.html`](../lichen_lff1.html)
9. [`lichen_lff2.html`](../lichen_lff2.html)
10. [`lichen_lff3.html`](../lichen_lff3.html)
11. [`lichen_lff4.html`](../lichen_lff4.html)
12. [`nar_2023_home.html`](../nar_2023_home.html)
13. [`species_accession.html`](../species_accession.html)
14. [`taxa_search.html`](../taxa_search.html)

## Recommendations

1. **Video Format**: MP4 (H.264 codec) is the most widely supported format across browsers. Converting the `.mov` file is the best solution.

2. **Emoji Alternatives**: If visual indicators are desired:
   - Use CSS icons or Font Awesome icons instead of emojis
   - Use Bootstrap icons (already included in the project)
   - Add descriptive text without symbols

3. **Future Considerations**: 
   - Establish a style guide for button text (with or without icons)
   - Test all features in deployment environment before going live
   - Consider using SVG icons for better cross-platform consistency

## Completion Criteria

- [ ] Video plays successfully in browser modal on crmA page
- [ ] All emojis removed from button text across all pages
- [ ] All buttons remain functional after text changes
- [ ] Website tested in deployment environment
- [ ] Changes verified across multiple browsers
