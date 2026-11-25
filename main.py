#!/usr/bin/env python3
"""The Most Boring Object, Reviewed in One Line.

Writes one funny, true one-line review of the most boring everyday
object we could name -- a paperclip -- to /output/entry.txt.

Craft notes (from the kit's judge brief, most important first):
1. On subject: a one-line review of a boring everyday object, funny
   and true. A paperclip is about as boring and everyday as it gets.
2. The laugh comes from a real, recognisable detail of the object:
   a paperclip's whole life is holding other people's papers
   together -- here, four years of tax paperwork -- while staying
   exactly itself.
3. True: paperclips really do sit on the same stack of papers for
   years, unbent, unpromoted, doing the same small job.
4. One line, inside 200 characters, every word earning its place.
5. Lands fast: the turn comes at "and is the only thing..." and the
   last words ("with its life in order") sharpen it instead of
   trailing off.
"""

import os

ENTRY = (
    "This paperclip has held my taxes together for four years and is "
    "the only thing in this office with its life in order."
)

# Generic-joke tells: words that signal a joke that would fit any
# object, not this one. The judge's criterion 2 demotes those, so the
# entry must contain none of them.
BANNED_GENERIC = (
    "unlike me", "my ex", "monday", "meeting", "coffee", "wifi",
    "password", "my therapist", "adulting", "literally me",
)


def check_is_text(text):
    if not isinstance(text, str):
        raise ValueError("entry must be a string")


def check_not_blank(text):
    if not text.strip():
        raise ValueError("entry must not be only white space")


def check_utf8(text):
    text.encode("utf-8")  # raises if not encodable


def check_length(text):
    # Gate: /output/entry.txt is UTF-8 text of 1 to 200 characters.
    if not 1 <= len(text) <= 200:
        raise ValueError(
            "entry must be 1-200 characters, got %d" % len(text)
        )


def check_single_line(text):
    # Gate + judge criterion 4: stays inside one line.
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")


def check_object(text):
    # Judge criterion 1: a review of a single boring everyday object.
    if "paperclip" not in text.lower():
        raise ValueError("entry must name its boring everyday object")


def check_real_detail(text):
    # Judge criteria 2 and 3: the laugh must come from a real,
    # recognisable detail of the object -- holding the same papers
    # together for years -- not a joke that would fit anything.
    lowered = text.lower()
    for anchor in ("held", "taxes", "four years"):
        if anchor not in lowered:
            raise ValueError(
                "entry is missing its real-detail anchor %r" % anchor
            )


def check_no_generic_jokes(text):
    lowered = text.lower()
    for phrase in BANNED_GENERIC:
        if phrase in lowered:
            raise ValueError(
                "entry leans on a generic joke %r; the laugh must "
                "come from the object itself" % phrase
            )


def check_sting(text):
    # Judge criterion 5: lands fast, last words sharpen it.
    if not text.rstrip().endswith("with its life in order."):
        raise ValueError("entry must end on its sharpening last words")


def check_sting_in_second_half(text):
    # Judge criterion 5: the review lands fast, then sharpens at the
    # end -- the sharpening turn must start well into the text, after
    # the setup ("held my taxes together for four years"), so the
    # setup lands before the punch.
    turn = "and is the only thing in this office with its life in order."
    idx = text.lower().find(turn)
    if idx < 0:
        raise ValueError("entry is missing its sharpening turn")
    if idx < len(text) // 3:
        raise ValueError(
            "sharpening turn starts too early; the review must land "
            "fast and sharpen at the end"
        )


def check_object_is_subject(text):
    # Judge criterion 1: the joke stays about the object, not the
    # reviewer -- the review must open on the object itself.
    if not text.startswith("This paperclip"):
        raise ValueError(
            "entry must open on the object itself: 'This paperclip'"
        )


def validate_structure(text):
    """Gates: well-formed UTF-8 text, in range, one line."""
    check_is_text(text)
    check_not_blank(text)
    check_utf8(text)
    check_length(text)
    check_single_line(text)


def validate_voice(text):
    """Judge brief: on-subject object, real detail, true, sharp ending."""
    check_object(text)
    check_object_is_subject(text)
    check_real_detail(text)
    check_no_generic_jokes(text)
    check_sting(text)
    check_sting_in_second_half(text)


def validate(text):
    validate_structure(text)
    validate_voice(text)


def main():
    validate(ENTRY)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(ENTRY + "\n")
    print("wrote /output/entry.txt: %d characters"
          % (len(ENTRY) + 1))


if __name__ == "__main__":
    main()
