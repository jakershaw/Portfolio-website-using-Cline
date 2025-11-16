# Image Embedding Guide

## Overview

This guide explains the new image embedding functionality for project content and the updated admin interface.

## New Features

### 1. Content Image Embedding

You can now upload multiple images and embed them within your project content using Markdown syntax.

#### How to Use:

1. **Navigate to Project Form**: Go to Admin Dashboard → Create Project (or Edit Project)

2. **Upload Content Images**: 
   - Scroll down to the "Content Images" field
   - Click "Choose Files" and select one or more images (JPG, PNG, or GIF)
   - Upload multiple images at once

3. **Copy Image Paths**:
   - After uploading, the form will display all uploaded images with their paths
   - Each image shows a thumbnail and a Markdown snippet like:
     ```markdown
     ![Image description](/static/uploads/projects/content/20250125_100000_image.jpg)
     ```

4. **Embed in Content**:
   - Copy the Markdown snippet
   - Paste it into your "Project Content" field where you want the image to appear
   - Customize the image description text as needed

#### Example Usage:

```markdown
# My Project

This is the introduction to my project.

![Screenshot of the application](/static/uploads/projects/content/20250125_100000_screenshot.png)

Here's how the feature works...

![Diagram showing architecture](/static/uploads/projects/content/20250125_100100_diagram.png)
```

### 2. Profile Image Hidden on Admin Pages

The profile photo and display name are now automatically hidden when you're on any admin page:
- Admin Dashboard
- Edit Profile
- Create/Edit Project

This provides a cleaner, more focused admin interface while maintaining the profile display on public pages.

## Database Migration

**IMPORTANT**: Before using the new content image feature, you must run the migration script to update your database.

### Running the Migration:

```bash
# Navigate to the project directory
cd "path/to/portfolio-website"

# Run the migration script
python migrate_add_content_images.py
```

The script will:
- Check if the `content_images` field already exists
- Add the field if it doesn't exist
- Confirm successful migration

### Migration Output:

```
Starting database migration...
============================================================
Adding content_images column to Project table...
✓ Migration completed successfully!
  - Added content_images field to Project model

You can now upload content images when creating/editing projects.
============================================================
```

## Technical Details

### Database Changes

- **New Field**: `content_images` (TEXT) in the `project` table
- **Format**: JSON array of image paths
- **Default**: Empty array `[]`

### File Storage

- **Content Images Location**: `app/static/uploads/projects/content/`
- **Naming Convention**: `YYYYMMDD_HHMMSS_originalname.ext`
- **Allowed Formats**: JPG, JPEG, PNG, GIF

### Form Updates

- **New Field**: `content_images` (MultipleFileField)
- **Validation**: File type checking (images only)
- **Display**: Thumbnails with copy-able Markdown snippets

## Tips and Best Practices

### Image Optimization

1. **Size**: Keep images under 2MB for faster loading
2. **Dimensions**: Resize images appropriately before upload
3. **Format**: Use JPEG for photos, PNG for graphics/screenshots

### Markdown Formatting

You can control image display using HTML if needed:

```markdown
<!-- Center an image -->
<div style="text-align: center;">
  ![Centered image](/static/uploads/projects/content/image.png)
</div>

<!-- Set image width -->
<img src="/static/uploads/projects/content/image.png" alt="Description" width="500">
```

### Content Organization

1. Upload all images at once when creating/editing a project
2. Use descriptive filenames before uploading
3. Keep track of which images are used in each project
4. Add meaningful alt text descriptions

## Troubleshooting

### Images Not Displaying

1. **Check Path**: Ensure the path starts with `/static/uploads/...`
2. **File Permissions**: Verify upload directory is writable
3. **File Type**: Confirm image is JPG, JPEG, PNG, or GIF

### Upload Issues

1. **File Size**: Check if image exceeds server limits
2. **Directory**: Ensure `app/static/uploads/projects/content/` exists
3. **Permissions**: Verify write permissions on upload directory

### Migration Issues

If migration fails:
1. Check database file permissions
2. Ensure no other process is using the database
3. Verify app configuration is correct
4. Check `migrate_add_content_images.py` for error messages

## Example Workflow

1. **Create New Project**:
   - Navigate to Admin Dashboard
   - Click "Create Project"
   - Fill in title, description, and initial content

2. **Upload Content Images**:
   - Select multiple images in "Content Images" field
   - Click "Save Project"

3. **Edit and Embed**:
   - Click "Edit" on the project
   - Copy image paths from "Existing Content Images" section
   - Paste into content where needed
   - Save changes

4. **Preview**:
   - View the project on the public site
   - Verify images display correctly
   - Check markdown formatting

## Support

For issues or questions:
- Check the console for error messages
- Review flask logs for detailed information
- Ensure all dependencies are up to date
