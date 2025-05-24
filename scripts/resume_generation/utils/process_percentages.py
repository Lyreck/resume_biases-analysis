import re

def escape_percent_in_tex(tex):

    # Replace % that are not at the start of a line with \%
    updated_content =re.sub(r'(?<=\d)%', r'\\%', tex, flags=re.MULTILINE)

    return updated_content


if __name__ == "__main__":
    #example usage

    tex_file = r'''\documentclass[letterpaper,11pt]{article}
    \usepackage[empty]{fullpage}
    \usepackage[hidelinks]{hyperref}
    \usepackage{fancyhdr}
    \pagestyle{fancy}
    \fancyhf{}
    \renewcommand{\headrulewidth}{0pt}
    \renewcommand{\footrulewidth}{0pt}
    \begin{document}

    %----------HEADING----------
    \begin{center}
        \textbf{\Huge \scshape {name}} \\ \vspace{1pt}
        \small Gender: {gender} $|$ Company: {company} $|$ Association: {association}
    \end{center}

    We know that 50% of the people are not happy with this. But 100% of the people are happy with this.
    % This is a comment % This is not a comment

    \end{document}'''

    updated_tex = escape_percent_in_tex(tex_file)
    print(updated_tex)


    # Check if newlines are present
    print("Inspecting newlines:")
    print(repr(tex_file))  # Shows the raw string with escape characters

    print("\nIterating through lines:")
    for line in tex_file.splitlines():
        print(f"Line: {repr(line)}")

