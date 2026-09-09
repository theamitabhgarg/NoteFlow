import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Icon({ name, size = 20 }) {
  const common = {
    width: size,
    height: size,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "1.8",
    strokeLinecap: "round",
    strokeLinejoin: "round",
  };

  const icons = {
    leaf: (
      <svg {...common} viewBox="0 0 32 32">
        <path d="M27.5 4.5C17 5 8.1 9.2 5.7 17.1c-1.2 4 .4 7.5 3.8 9.1 3.4 1.6 7.7.3 10.5-2.3C25.3 18.8 27.1 11.7 27.5 4.5Z" />
        <path d="M6.5 26.5C11 19.8 16.2 14.7 24.7 8.5" />
      </svg>
    ),

    arrowLeft: (
      <svg {...common}>
        <path d="M19 12H5" />
        <path d="m12 19-7-7 7-7" />
      </svg>
    ),

    save: (
      <svg {...common}>
        <path d="M5 3h11l3 3v15H5z" />
        <path d="M8 3v6h8V3" />
        <path d="M8 15h8" />
      </svg>
    ),

    tag: (
      <svg {...common}>
        <path d="m20.6 13.4-7.2 7.2a2 2 0 0 1-2.8 0L3.4 13.4a2 2 0 0 1-.6-1.4V5a2 2 0 0 1 2-2h7a2 2 0 0 1 1.4.6l7.4 7.4a2 2 0 0 1 0 2.4Z" />
        <circle cx="7.5" cy="7.5" r="1" />
      </svg>
    ),
  };

  return icons[name] || null;
}

function CreateNote() {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [tags, setTags] = useState("");

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleCreateNote = async (event) => {
    event.preventDefault();

    setError("");
    setLoading(true);

    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/login");
      return;
    }

    try {
      const tagsArray = tags
        .split(",")
        .map((tag) => tag.trim())
        .filter((tag) => tag !== "");

      const response = await fetch(
        "http://127.0.0.1:8000/notes",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },

          body: JSON.stringify({
            title: title.trim(),
            content: content.trim(),
            tags: tagsArray,
          }),
        }
      );

      const data = await response.json();

      console.log("Create note response:", data);

      if (!response.ok) {
        setError(
          data.detail ||
            "Failed to create note"
        );
        return;
      }

      navigate("/notes");
    } catch (error) {
      console.error(
        "Create note error:",
        error
      );

      setError(
        "Unable to connect to the server."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-page">

      {/* SIDEBAR */}

      <aside className="create-sidebar">

        <div className="create-brand">

          <div className="create-brand-icon">
            <Icon
              name="leaf"
              size={34}
            />
          </div>

          <div>
            <h1>NoteFlow</h1>

            <p>
              Write. Organize. Grow.
            </p>
          </div>

        </div>


        <div className="create-sidebar-content">

          <p className="create-sidebar-label">
            NEW NOTE
          </p>

          <h2>
            Put your thoughts
            <br />
            somewhere they
            <br />
            can grow.
          </h2>

          <p className="create-sidebar-description">
            Capture an idea, save something
            you learned, or simply write
            something worth remembering.
          </p>

        </div>


        <div className="create-sidebar-bottom">

          <span />

          <p>
            “The smallest note
            <br />
            can become the
            <br />
            biggest idea.”
          </p>

          <div className="create-sidebar-footer">

            <span>
              NoteFlow
            </span>

            <span>
              v1.0
            </span>

          </div>

        </div>

      </aside>


      {/* MAIN CONTENT */}

      <main className="create-main">

        {/* TOP NAVIGATION */}

        <header className="create-topbar">

          <button
            className="back-button"
            type="button"
            onClick={() =>
              navigate("/notes")
            }
          >

            <Icon
              name="arrowLeft"
              size={17}
            />

            Back to notes

          </button>

        </header>


        {/* FORM AREA */}

        <section className="create-content">

          <div className="create-heading">

            <p className="create-eyebrow">
              NEW ENTRY
            </p>

            <h2>
              Create a note
            </h2>

            <p>
              Write something worth
              remembering.
            </p>

          </div>


          <form
            className="create-form"
            onSubmit={
              handleCreateNote
            }
          >

            {/* TITLE */}

            <div className="create-field title-field">

              <label htmlFor="title">
                Title
              </label>

              <input
                type="text"
                id="title"
                value={title}
                onChange={(event) =>
                  setTitle(
                    event.target.value
                  )
                }
                placeholder="Give your note a title..."
                required
                autoFocus
              />

            </div>


            {/* CONTENT */}

            <div className="create-field content-field">

              <label htmlFor="content">
                Your note
              </label>

              <textarea
                id="content"
                value={content}
                onChange={(event) =>
                  setContent(
                    event.target.value
                  )
                }
                placeholder="Start writing here..."
                required
              />

              <div className="content-footer">

                <span>
                  {content.length} characters
                </span>

              </div>

            </div>


            {/* TAGS */}

            <div className="create-field tags-field">

              <label htmlFor="tags">
                Tags
              </label>

              <div className="tag-input-wrapper">

                <Icon
                  name="tag"
                  size={17}
                />

                <input
                  type="text"
                  id="tags"
                  value={tags}
                  onChange={(event) =>
                    setTags(
                      event.target.value
                    )
                  }
                  placeholder="e.g. learning, react, ideas"
                />

              </div>

              <small>
                Separate multiple tags with
                commas.
              </small>

            </div>


            {/* ERROR */}

            {error && (

              <div className="create-error">
                {error}
              </div>

            )}


            {/* ACTIONS */}

            <div className="create-actions">

              <button
                type="button"
                className="cancel-create-button"
                onClick={() =>
                  navigate("/notes")
                }
                disabled={loading}
              >
                Cancel
              </button>


              <button
                type="submit"
                className="save-note-button"
                disabled={loading}
              >

                <Icon
                  name="save"
                  size={18}
                />

                {loading
                  ? "Creating..."
                  : "Create Note"}

              </button>

            </div>

          </form>

        </section>

      </main>

    </div>
  );
}

export default CreateNote;