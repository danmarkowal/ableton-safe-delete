# Ableton Safe Delete

A CLI tool for finding unused sample packs.

Has your storage space ever been burdened by samplepacks you hoarded long ago? How are you to tell which samples you used, and from which packs across your hundreds of projects? This tool helps you identify those unused samples (grouped by samplepack) so you can safetly delete them without the fear of missing samples in your Ableton projects.

## How it works

1. You provide a reference to your samplepack directory as well as your root project directory (where your store all your projects).

2. The tool cross-checks which samples are used in which projects, and if so little as a single sample from a pack is used in so little as a single project, the pack is marked as in use, meaning it should not be deleted.

3. Finally, you are informed of which sub-folders CAN be safely deleted.

## Installation

```bash
git clone https://github.com/danmarkowal/ableton-safe-delete.git
cd ableton-safe-delete
pip3 install -e .
```

## Usage (Example)

It is useful to use the `-r` flag to recursively search through subdirectories of your project directory.

```bash
alsafedel -p "/Users/me/Projects" -s "/Users/me/Samplepacks" -r
```
