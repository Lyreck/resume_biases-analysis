## Take input .tex with {} and replace each of them with {{}}.


def double_placeholders(tex_file):
    """
    Replace single curly braces with double curly braces in the given .tex file.
    """
    # with open(tex_file, 'r') as file:
        # content = file.read()

    # Replace single curly braces with double curly braces
    content = tex_file.replace('{', '{{').replace('}', '}}')

    return content
    # with open(tex_file, 'w') as file:
    #     file.write(content)



if __name__ == "__main__":
    tex_file = r'''
    \documentclass[letterpaper,11pt]{article}
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

    \end{document}
    '''

    doubled = double_placeholders(tex_file)

    print(doubled)

