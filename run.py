import argparse
from dotenv import load_dotenv
from pathlib import Path
import os
import shutil
import subprocess
import tempfile
from story_beats_loom import loom


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("story_path")

    # Get list of storyformats
    path = "./tweego/storyformats"
    story_formats = os.listdir(path)
    parser.add_argument(
        "-l",
        "--llm",
        help="LLM provider",
        choices=["anthropic", "openai"],
        default="anthropic",
    )

    parser.add_argument(
        "-t",
        "--twine",
        help="Twine story format",
        choices=story_formats,
        default=None,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output folder",
        default=None,
    )
    parser.add_argument(
        "-j",
        "--json",
        help="JSON output",
        default=None,
    )

    args = parser.parse_args()
    load_dotenv()

    story_path = Path(args.story_path)
    story = loom.generate_story_from_outline(story_path, args.llm)

    # EXPORT:
    print("[+] Exporting generated story")
    filepath = Path(story_path)
    spec_dir = filepath.parent
    filename = filepath.stem

    # Always output to ink
    ink_fp = spec_dir / f"{filename}.ink"
    story.to_ink_file(ink_fp)
    print("[+] Story written to ink file:", ink_fp)
    
    # Copy rest of project file to folder
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = spec_dir / filename
        
    output_dir.mkdir(parents=True, exist_ok=True)
    ink_template_dir = Path("ink/template")
        
    for dirpath,_,filenames in os.walk(ink_template_dir):
        for f in filenames:
            shutil.copy2(os.path.abspath(os.path.join(dirpath, f)), output_dir)

    inkjs_fp = output_dir / "story.js"
    subprocess.call(["ink/inklecate", "-o", inkjs_fp, ink_fp])
    
    # Concat "var storyContent = " to make the file javascript runnable
    tmp_fp = output_dir / "story.js.tmp"
    with open(inkjs_fp,'r') as f:
        with open(tmp_fp, "w") as f2:
            f2.write("var storyContent = ")
            f2.write(f.read())
    os.remove(inkjs_fp)
    os.rename(tmp_fp, inkjs_fp)    

    if args.json:
        json_fp = spec_dir / f"{filename}.json"
        story.to_json_file(json_fp)
        print("[+] Story written to JSON file:", json_fp)

    if args.twine:
        if args.output:
            output_path = args.output
        else:
            output_path = spec_dir / filename / "index.html"

        twee_fp = spec_dir / f"{filename}.twee"
        story.to_twee3_file(twee_fp)
        print("[+] Story written to Twee3 file:", twee_fp)

        subprocess.call(["tweego/tweego", "-f", args.twine, "-o", output_path, twee_fp])
