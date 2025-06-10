####### This code allows to take as an input a normal .tex file and output a .tex file that allows us to use Python to input data in the template.
####### What it does is:
#######  1. Escape percent signs that are not at the start of a line (to avoid commenting some text that has "10% of ...", for example).
####### 2. double the curly braces, so that we can use them as placeholders for Python variables.

from .utils.double_placeholders import double_placeholders
from .utils.process_percentages import escape_percent_in_tex

def process_tex_string(tex_string):
    """
    Process the LaTeX string to escape special characters and double curly braces.
    """
    # Escape percent signs
    tex_string = escape_percent_in_tex(tex_string)
    
    # Double curly braces
    tex_string = double_placeholders(tex_string)
    
    return tex_string



if __name__ == "__main__":
    # Example usage

    # tex_template is the .tex code we wish to use - e.g. a template downloaded from Overleaf.
    tex_template = r'''%-------------------------
    % Resume in Latex
    % Author : Jake Gutierrez
    % Based off of: https://github.com/sb2nov/resume
    % License : MIT
    %------------------------

    \documentclass[letterpaper,11pt]{article}

    \usepackage{latexsym}
    \usepackage[empty]{fullpage}
    \usepackage{titlesec}
    \usepackage{marvosym}
    \usepackage[usenames,dvipsnames]{color}
    \usepackage{verbatim}
    \usepackage{enumitem}
    \usepackage[hidelinks]{hyperref}
    \usepackage{fancyhdr}
    \usepackage[english]{babel}
    \usepackage{tabularx}
    \input{glyphtounicode}


    %----------FONT OPTIONS----------
    % sans-serif
    % \usepackage[sfdefault]{FiraSans}
    % \usepackage[sfdefault]{roboto}
    % \usepackage[sfdefault]{noto-sans}
    % \usepackage[default]{sourcesanspro}

    % serif
    % \usepackage{CormorantGaramond}
    % \usepackage{charter}


    \pagestyle{fancy}
    \fancyhf{} % clear all header and footer fields
    \fancyfoot{}
    \renewcommand{\headrulewidth}{0pt}
    \renewcommand{\footrulewidth}{0pt}

    % Adjust margins
    \addtolength{\oddsidemargin}{-0.5in}
    \addtolength{\evensidemargin}{-0.5in}
    \addtolength{\textwidth}{1in}
    \addtolength{\topmargin}{-.5in}
    \addtolength{\textheight}{1.0in}

    \urlstyle{same}

    \raggedbottom
    \raggedright
    \setlength{\tabcolsep}{0in}

    % Sections formatting
    \titleformat{\section}{
      \vspace{-4pt}\scshape\raggedright\large
    }{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

    % Ensure that generate pdf is machine readable/ATS parsable
    \pdfgentounicode=1

    %-------------------------
    % Custom commands
    \newcommand{\resumeItem}[1]{
      \item\small{
        {#1 \vspace{-2pt}}
      }
    }

    \newcommand{\resumeSubheading}[4]{
      \vspace{-2pt}\item
        \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
          \textbf{#1} & #2 \\
          \textit{\small#3} & \textit{\small #4} \\
        \end{tabular*}\vspace{-7pt}
    }

    \newcommand{\resumeSubSubheading}[2]{
        \item
        \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
          \textit{\small#1} & \textit{\small #2} \\
        \end{tabular*}\vspace{-7pt}
    }

    \newcommand{\resumeProjectHeading}[2]{
        \item
        \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
          \small#1 & #2 \\
        \end{tabular*}\vspace{-7pt}
    }

    \newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}

    \renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

    \newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
    \newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
    \newcommand{\resumeItemListStart}{\begin{itemize}}
    \newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

    %-------------------------------------------
    %%%%%%  RESUME STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%


    \begin{document}

    %----------HEADING----------
    % \begin{tabular*}{\textwidth}{l@{\extracolsep{\fill}}r}
    %   \textbf{\href{http://sourabhbajaj.com/}{\Large Sourabh Bajaj}} & Email : \href{mailto:sourabh@sourabhbajaj.com}{sourabh@sourabhbajaj.com}\\
    %   \href{http://sourabhbajaj.com/}{http://www.sourabhbajaj.com} & Mobile : +1-123-456-7890 \\
    % \end{tabular*}

    \begin{center}
        \textbf{\Huge \scshape Jake Ryan} \\ \vspace{1pt}
        \small 123-456-7890 $|$ \href{mailto:x@x.com}{\underline{jake@su.edu}} $|$ 
        \href{https://linkedin.com/in/...}{\underline{linkedin.com/in/jake}} $|$
        \href{https://github.com/...}{\underline{github.com/jake}}
    \end{center}


    %-----------EDUCATION-----------
    \section{Education}
      \resumeSubHeadingListStart
        \resumeSubheading
          {Southwestern University}{Georgetown, TX}
          {Bachelor of Arts in Computer Science, Minor in Business}{Aug. 2018 -- May 2021}
        \resumeSubheading
          {Blinn College}{Bryan, TX}
          {Associate's in Liberal Arts}{Aug. 2014 -- May 2018}
      \resumeSubHeadingListEnd


    %-----------EXPERIENCE-----------
    \section{Experience}
      \resumeSubHeadingListStart

        \resumeSubheading
          {Undergraduate Research Assistant}{June 2020 -- Present}
          {Texas A\&M University}{College Station, TX}
          \resumeItemListStart
            \resumeItem{Developed a REST API using FastAPI and PostgreSQL to store data from learning management systems}
            \resumeItem{Developed a full-stack web application using Flask, React, PostgreSQL and Docker to analyze GitHub data}
            \resumeItem{Explored ways to visualize GitHub collaboration in a classroom setting}
          \resumeItemListEnd
          
    % -----------Multiple Positions Heading-----------
    %    \resumeSubSubheading
    %     {Software Engineer I}{Oct 2014 - Sep 2016}
    %     \resumeItemListStart
    %        \resumeItem{Apache Beam}
    %          {Apache Beam is a unified model for defining both batch and streaming data-parallel processing pipelines}
    %     \resumeItemListEnd
    %    \resumeSubHeadingListEnd
    %-------------------------------------------

        \resumeSubheading
          {Information Technology Support Specialist}{Sep. 2018 -- Present}
          {Southwestern University}{Georgetown, TX}
          \resumeItemListStart
            \resumeItem{Communicate with managers to set up campus computers used on campus}
            \resumeItem{Assess and troubleshoot computer problems brought by students, faculty and staff}
            \resumeItem{Maintain upkeep of computers, classroom equipment, and 200 printers across campus}
        \resumeItemListEnd

        \resumeSubheading
          {Artificial Intelligence Research Assistant}{May 2019 -- July 2019}
          {Southwestern University}{Georgetown, TX}
          \resumeItemListStart
            \resumeItem{Explored methods to generate video game dungeons based off of \emph{The Legend of Zelda}}
            \resumeItem{Developed a game in Java to test the generated dungeons}
            \resumeItem{Contributed 50K+ lines of code to an established codebase via Git}
            \resumeItem{Conducted  a human subject study to determine which video game dungeon generation technique is enjoyable}
            \resumeItem{Wrote an 8-page paper and gave multiple presentations on-campus}
            \resumeItem{Presented virtually to the World Conference on Computational Intelligence}
          \resumeItemListEnd

      \resumeSubHeadingListEnd


    %-----------PROJECTS-----------
    \section{Projects}
        \resumeSubHeadingListStart
          \resumeProjectHeading
              {\textbf{Gitlytics} $|$ \emph{Python, Flask, React, PostgreSQL, Docker}}{June 2020 -- Present}
              \resumeItemListStart
                \resumeItem{Developed a full-stack web application using with Flask serving a REST API with React as the frontend}
                \resumeItem{Implemented GitHub OAuth to get data from user’s repositories}
                \resumeItem{Visualized GitHub data to show collaboration}
                \resumeItem{Used Celery and Redis for asynchronous tasks}
              \resumeItemListEnd
          \resumeProjectHeading
              {\textbf{Simple Paintball} $|$ \emph{Spigot API, Java, Maven, TravisCI, Git}}{May 2018 -- May 2020}
              \resumeItemListStart
                \resumeItem{Developed a Minecraft server plugin to entertain kids during free time for a previous job}
                \resumeItem{Published plugin to websites gaining 2K+ downloads and an average 4.5/5-star review}
                \resumeItem{Implemented continuous delivery using TravisCI to build the plugin upon new a release}
                \resumeItem{Collaborated with Minecraft server administrators to suggest features and get feedback about the plugin}
              \resumeItemListEnd
        \resumeSubHeadingListEnd



      %
      %-----------PROGRAMMING SKILLS-----------
      %\section{Technical Skills}
      % \begin{itemize}[leftmargin=0.15in, label={}]
      %    \small{\item{
      %     \textbf{Languages}{: Java, Python, C/C++, SQL (Postgres), JavaScript, HTML/CSS, R} \\
      %     \textbf{Frameworks}{: React, Node.js, Flask, JUnit, WordPress, Material-UI, FastAPI} \\
      %     \textbf{Developer Tools}{: Git, Docker, TravisCI, Google Cloud Platform, VS Code, Visual Studio, PyCharm, IntelliJ, Eclipse} \\
      %     \textbf{Libraries}{: pandas, NumPy, Matplotlib}
      %    }}
      % \end{itemize}


      %-------------------------------------------
      \end{document}'''
    
    ## Pre processing of the original tex file (change {} into {{}} and % into \%)
    tex_template = process_tex_string(tex_template)
    with open("data/tex_template.tex", "w") as f: #generate the file in the data directory.
        f.write(tex_template)