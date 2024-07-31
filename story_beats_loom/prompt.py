def generate_prompt(cumulative_text, genre, pov, setting, style, tone, plot):
    system = f"""
You are an award winning novelist in the genre of {genre}.
You will be writing interactive fiction story based on a given a setting and story beat, in {pov} view.
"""

    prompt = f"""
The setting of the story is as follows:
<setting>
{setting}
</setting>

Assume the tone of {tone}.
Write in the style of {style}.

This is the story that has been written so far:
<existing_story>
{cumulative_text}
</existing_story>

Write prose to continue the story, following this story beat closely:
<beat>
{plot}
</beat>

"""
    return system, prompt
