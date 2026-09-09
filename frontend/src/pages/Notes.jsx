import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./NotesFeatures.css";

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
    home: (
      <svg {...common}>
        <path d="M3 10.5 12 3l9 7.5" />
        <path d="M5 9.5V21h14V9.5" />
        <path d="M9 21v-6h6v6" />
      </svg>
    ),

    notes: (
      <svg {...common}>
        <rect x="4" y="3" width="16" height="18" rx="2" />
        <path d="M8 8h8M8 12h8M8 16h5" />
      </svg>
    ),

    tag: (
      <svg {...common}>
        <path d="m20.6 13.4-7.2 7.2a2 2 0 0 1-2.8 0L3.4 13.4a2 2 0 0 1-.6-1.4V5a2 2 0 0 1 2-2h7a2 2 0 0 1 1.4.6l7.4 7.4a2 2 0 0 1 0 2.4Z" />
        <circle cx="7.5" cy="7.5" r="1" />
      </svg>
    ),

    chart: (
      <svg {...common}>
        <path d="M4 20V10" />
        <path d="M10 20V4" />
        <path d="M16 20v-7" />
        <path d="M22 20V7" />
      </svg>
    ),

    search: (
      <svg {...common}>
        <circle cx="11" cy="11" r="7" />
        <path d="m20 20-4-4" />
      </svg>
    ),

    plus: (
      <svg {...common}>
        <path d="M12 5v14M5 12h14" />
      </svg>
    ),

    settings: (
      <svg {...common}>
        <path d="M4 7h16" />
        <circle cx="9" cy="7" r="2" />
        <path d="M4 12h16" />
        <circle cx="15" cy="12" r="2" />
        <path d="M4 17h16" />
        <circle cx="11" cy="17" r="2" />
      </svg>
    ),

    calendar: (
      <svg {...common}>
        <rect x="3" y="5" width="18" height="16" rx="2" />
        <path d="M16 3v4M8 3v4M3 10h18" />
      </svg>
    ),

    comment: (
      <svg {...common}>
        <path d="M20 11.5a7.5 7.5 0 0 1-8 7.5 8.8 8.8 0 0 1-3.7-.8L4 20l1.3-3.4A7.3 7.3 0 0 1 4 12a7.5 7.5 0 0 1 8-7.5 7.5 7.5 0 0 1 8 7Z" />
      </svg>
    ),

    thumb: (
      <svg {...common}>
        <path d="M7 10v10H4a2 2 0 0 1-2-2v-6a2 2 0 0 1 2-2h3Z" />
        <path d="M7 20h8.5a2 2 0 0 0 1.9-1.4l2-6A2 2 0 0 0 17.5 10H14l.5-3.5A2.1 2.1 0 0 0 12.4 4L7 10" />
      </svg>
    ),

    trash: (
      <svg {...common}>
        <path d="M4 7h16" />
        <path d="M10 11v6M14 11v6" />
        <path d="M6 7l1 14h10l1-14" />
        <path d="M9 7V4h6v3" />
      </svg>
    ),

    more: (
      <svg {...common}>
        <circle cx="5" cy="12" r="1" fill="currentColor" />
        <circle cx="12" cy="12" r="1" fill="currentColor" />
        <circle cx="19" cy="12" r="1" fill="currentColor" />
      </svg>
    ),

    arrow: (
      <svg {...common}>
        <path d="m6 9 6 6 6-6" />
      </svg>
    ),

    leaf: (
      <svg
        {...common}
        viewBox="0 0 32 32"
        strokeWidth="1.7"
      >
        <path d="M27.5 4.5C17 5 8.1 9.2 5.7 17.1c-1.2 4 .4 7.5 3.8 9.1 3.4 1.6 7.7.3 10.5-2.3C25.3 18.8 27.1 11.7 27.5 4.5Z" />
        <path d="M6.5 26.5C11 19.8 16.2 14.7 24.7 8.5" />
      </svg>
    ),

    user: (
      <svg {...common}>
        <circle cx="12" cy="8" r="4" />
        <path d="M4 21c.8-4 3.4-6 8-6s7.2 2 8 6" />
      </svg>
    ),

    logout: (
      <svg {...common}>
        <path d="M10 4H5a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h5" />
        <path d="m15 16 4-4-4-4" />
        <path d="M19 12H9" />
      </svg>
    ),

    sort: (
      <svg {...common}>
        <path d="M8 6h12" />
        <path d="M8 12h9" />
        <path d="M8 18h6" />
        <path d="M4 5v14" />
      </svg>
    ),
  };

  return icons[name] || null;
}


function getNoteId(note) {
  return note.id || note._id;
}


function formatDate(dateValue) {
  if (!dateValue) {
    return "Recently";
  }

  const date = new Date(dateValue);

  if (Number.isNaN(date.getTime())) {
    return "Recently";
  }

  return date.toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}


function getUserFromToken() {
  const token = localStorage.getItem("token");

  if (!token) {
    return {
      username: "User",
      userId: null,
      role: "user",
    };
  }

  try {
    const payload = JSON.parse(
      atob(token.split(".")[1])
    );

    return {
      username: payload.username || "User",
      userId: payload.user_id || null,
      role: payload.role || "user",
    };
  } catch {
    return {
      username: "User",
      userId: null,
      role: "user",
    };
  }
}


function Sidebar({
  activeSection,
  sidebarCollapsed,
  onToggle,
  onNavigate,
  isAdmin = false,
}) {
  return (
    <aside className="sidebar">
      <button
        type="button"
        className="sidebar-collapse-button"
        onClick={onToggle}
        aria-label={
          sidebarCollapsed
            ? "Expand sidebar"
            : "Collapse sidebar"
        }
        title={
          sidebarCollapsed
            ? "Expand sidebar"
            : "Collapse sidebar"
        }
      >
        <Icon name="arrow" size={16} />
      </button>

      <div className="brand">
        <div className="brand-mark">
          <Icon name="leaf" size={31} />
        </div>
        <div className="sidebar-expand-content">
          <h1>NoteFlow</h1>
          <p>Write. Organize. Grow.</p>
        </div>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section-title sidebar-expand-content">
          WORKSPACE
        </div>

        <button
          className={activeSection === "all" ? "nav-item active" : "nav-item"}
          onClick={() => onNavigate("all")}
          title="All Notes"
        >
          <Icon name="home" />
          <span className="sidebar-expand-content">All Notes</span>
        </button>

        <button
          className={activeSection === "my" ? "nav-item active" : "nav-item"}
          onClick={() => onNavigate("my")}
          title="My Notes"
        >
          <Icon name="notes" />
          <span className="sidebar-expand-content">My Notes</span>
        </button>

        <button
          className={activeSection === "tags" ? "nav-item active" : "nav-item"}
          onClick={() => onNavigate("tags")}
          title="Tags"
        >
          <Icon name="tag" />
          <span className="sidebar-expand-content">Tags</span>
        </button>

        <button
          className={activeSection === "statistics" ? "nav-item active" : "nav-item"}
          onClick={() => onNavigate("statistics")}
          title="Statistics"
        >
          <Icon name="chart" />
          <span className="sidebar-expand-content">Statistics</span>
        </button>

        {isAdmin && (
          <button
            className={activeSection === "settings" ? "nav-item active" : "nav-item"}
            onClick={() => onNavigate("settings")}
            title="Settings"
          >
            <Icon name="settings" />
            <span className="sidebar-expand-content">Settings</span>
          </button>
        )}
      </nav>

      <div className="sidebar-divider" />

      <div className="sidebar-quote sidebar-expand-content">
        <p>
          “A better you
          <br />
          starts with
          <br />
          a note.”
        </p>
        <span />
      </div>

      <div className="sidebar-decoration sidebar-expand-content">❧</div>

      <div className="sidebar-footer sidebar-expand-content">
        <span>NoteFlow</span>
        <span>v1.0</span>
      </div>
    </aside>
  );
}


function ProfileMenu({
  currentUser,
  profileOpen,
  onToggle,
  onNavigate,
  onLogout,
}) {
  return (
    <div className="profile-container">
      <button
        type="button"
        className="user-avatar-button"
        onClick={onToggle}
        aria-label="Open profile menu"
        title={currentUser.username}
      >
        {currentUser.username
          .charAt(0)
          .toUpperCase()}
      </button>

      {profileOpen && (
        <div className="profile-dropdown profile-dropdown-minimal">
          <div className="dropdown-user minimal-dropdown-user">
            <div className="dropdown-avatar">
              {currentUser.username
                .charAt(0)
                .toUpperCase()}
            </div>

            <div>
              <strong>{currentUser.username}</strong>
              <span>Signed in</span>
            </div>
          </div>

          <div className="dropdown-divider" />

          <button
            type="button"
            className="dropdown-item"
            onClick={() => onNavigate("my")}
          >
            <Icon name="user" size={17} />
            My Notes
          </button>

          <button
            type="button"
            className="dropdown-item logout-item"
            onClick={onLogout}
          >
            <Icon name="logout" size={17} />
            Logout
          </button>
        </div>
      )}
    </div>
  );
}


function SettingsPage({
  currentUser,
  darkMode,
  onToggleDarkMode,
  sidebarCollapsed,
  onToggleSidebar,
  onNavigate,
  profileOpen,
  onToggleProfile,
  onLogout,
}) {
  const [newUsername, setNewUsername] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [createUserMessage, setCreateUserMessage] = useState("");
  const [createUserError, setCreateUserError] = useState("");
  const [creatingUser, setCreatingUser] = useState(false);

  const handleCreateUser = async (event) => {
    event.preventDefault();

    const username = newUsername.trim();

    if (!username || !newPassword) {
      setCreateUserError("Username and password are required.");
      setCreateUserMessage("");
      return;
    }

    const token = localStorage.getItem("token");

    if (!token) {
      onLogout();
      return;
    }

    setCreatingUser(true);
    setCreateUserError("");
    setCreateUserMessage("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/admin/users",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            username,
            password: newPassword,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        if (response.status === 401) {
          onLogout();
          return;
        }

        setCreateUserError(
          data.detail || "Unable to create user."
        );
        return;
      }

      setCreateUserMessage(
        `User "${data.username}" created successfully.`
      );
      setNewUsername("");
      setNewPassword("");
    } catch (error) {
      console.error("Create user error:", error);
      setCreateUserError(
        "Unable to connect to the server. Please try again."
      );
    } finally {
      setCreatingUser(false);
    }
  };

  if (currentUser.role !== "admin") {
    return (
      <div className="dashboard">
        <Sidebar
          activeSection="all"
          sidebarCollapsed={sidebarCollapsed}
          onToggle={onToggleSidebar}
          onNavigate={onNavigate}
        />
        <div className="main-area">
          <main className="notes-content settings-page">
            <div className="settings-access-denied">
              <h2>Access denied</h2>
              <p>Only administrators can access settings.</p>
            </div>
          </main>
        </div>
      </div>
    );
  }

  return (
    <div
      className={`dashboard ${sidebarCollapsed ? "sidebar-collapsed" : ""} ${darkMode ? "theme-dark" : ""}`}
    >
      <Sidebar
        activeSection="settings"
        sidebarCollapsed={sidebarCollapsed}
        onToggle={onToggleSidebar}
        onNavigate={onNavigate}
        isAdmin={currentUser.role === "admin"}
      />

      <div className="main-area">
        <header className="topbar">
          <div className="topbar-spacer" />

          <div className="topbar-actions settings-topbar-actions">
            <ProfileMenu
              currentUser={currentUser}
              profileOpen={profileOpen}
              onToggle={onToggleProfile}
              onNavigate={onNavigate}
              onLogout={onLogout}
            />
          </div>
        </header>

        <main className="notes-content settings-page">
          <div className="page-heading">
            <div>
              <p className="eyebrow">ADMINISTRATION</p>
              <h2>Settings</h2>
              <p className="page-description">
                Manage your NoteFlow preferences and users.
              </p>
            </div>
          </div>

          <div className="settings-page-grid">
            <section className="settings-page-card">
              <div className="settings-page-card-icon">
                <Icon name="settings" size={22} />
              </div>

              <div className="settings-page-card-heading">
                <h3>Appearance</h3>
                <p>
                  Choose how the NoteFlow workspace looks on your screen.
                </p>
              </div>

              <div className="settings-page-divider" />

              <div className="settings-page-row">
                <div>
                  <strong>Dark mode</strong>
                  <span>
                    Use a darker appearance for the workspace.
                  </span>
                </div>

                <button
                  type="button"
                  className={
                    darkMode
                      ? "theme-switch on"
                      : "theme-switch"
                  }
                  onClick={onToggleDarkMode}
                  role="switch"
                  aria-checked={darkMode}
                  aria-label="Toggle dark mode"
                >
                  <span className="theme-switch-knob" />
                </button>
              </div>
            </section>

            <section className="settings-page-card">
              <div className="settings-page-card-icon">
                <Icon name="user" size={22} />
              </div>

              <div className="settings-page-card-heading">
                <h3>Create a new user</h3>
                <p>
                  Add a standard NoteFlow account. New accounts are created
                  with the user role.
                </p>
              </div>

              <div className="settings-page-divider" />

              <form
                className="admin-create-user-page-form"
                onSubmit={handleCreateUser}
              >
                <label>
                  <span>Username</span>
                  <input
                    type="text"
                    placeholder="Enter username"
                    value={newUsername}
                    onChange={(event) =>
                      setNewUsername(event.target.value)
                    }
                    autoComplete="off"
                  />
                </label>

                <label>
                  <span>Password</span>
                  <input
                    type="password"
                    placeholder="Enter temporary password"
                    value={newPassword}
                    onChange={(event) =>
                      setNewPassword(event.target.value)
                    }
                    autoComplete="new-password"
                  />
                </label>

                <button
                  type="submit"
                  className="admin-create-user-page-button"
                  disabled={creatingUser}
                >
                  {creatingUser ? "Creating user..." : "Create User"}
                </button>
              </form>

              {createUserMessage && (
                <p className="admin-create-user-success">
                  {createUserMessage}
                </p>
              )}

              {createUserError && (
                <p className="admin-create-user-error">
                  {createUserError}
                </p>
              )}
            </section>
          </div>
        </main>
      </div>
    </div>
  );
}


function Notes() {
  const [notes, setNotes] = useState([]);

  const [stats, setStats] = useState({
    notes_count: 0,
    unique_tags: 0,
    upvotes_given: 0,
    comments_written: 0,
    tag_counts: {},
  });

  const [expandedNote, setExpandedNote] = useState(null);

  const [comments, setComments] = useState({});
  const [commentCounts, setCommentCounts] = useState({});
  const [commentText, setCommentText] = useState({});
  const [commentErrors, setCommentErrors] = useState({});
  const [commentSubmitting, setCommentSubmitting] = useState({});
  const [upvotedNotes, setUpvotedNotes] = useState({});

  const [editingNote, setEditingNote] = useState(null);

  const [editTitle, setEditTitle] = useState("");
  const [editContent, setEditContent] = useState("");
  const [editTags, setEditTags] = useState("");

  const [searchText, setSearchText] = useState("");

  const [activeSection, setActiveSection] = useState("all");

  const [selectedTag, setSelectedTag] = useState("all");

  // NEW: sorting
  const [sortOrder, setSortOrder] =
    useState("newest");

  // NEW: profile dropdown
  const [profileOpen, setProfileOpen] =
    useState(false);

  // NEW: collapsible sidebar
  const [sidebarCollapsed, setSidebarCollapsed] =
    useState(false);

  // Dark mode
  const [darkMode, setDarkMode] = useState(() =>
    localStorage.getItem("noteflow-theme") === "dark"
  );

  const [loading, setLoading] = useState(true);
  const [commentsLoading, setCommentsLoading] =
    useState({});
  const [savingEdit, setSavingEdit] =
    useState(false);

  const [error, setError] = useState("");

  // Server-side pagination
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalNotes, setTotalNotes] = useState(0);
  const NOTES_PER_PAGE = 8;

  const [allTags, setAllTags] = useState([]);

  const navigate = useNavigate();

  const currentUser = getUserFromToken();


  useEffect(() => {
    localStorage.setItem(
      "noteflow-theme",
      darkMode ? "dark" : "light"
    );
  }, [darkMode]);


  /*
    Fetch notes using server-side pagination.
  */

  useEffect(() => {
    if (
      activeSection === "statistics" ||
      activeSection === "settings"
    ) {
      return;
    }

    const fetchNotes = async () => {
      const token = localStorage.getItem("token");

      if (!token) {
        navigate("/login");
        return;
      }

      try {
        const params = new URLSearchParams({
          page: String(currentPage),
          limit: String(NOTES_PER_PAGE),
          sort: sortOrder,
        });

        if (searchText.trim()) {
          params.set("search", searchText.trim());
        }

        if (selectedTag !== "all") {
          params.set("tag", selectedTag);
        }

        const endpoint =
          activeSection === "my"
            ? "http://127.0.0.1:8000/notes/mine"
            : "http://127.0.0.1:8000/notes";

        const response = await fetch(
          `${endpoint}?${params.toString()}`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        const data = await response.json();

        if (!response.ok) {
          if (response.status === 401) {
            localStorage.removeItem("token");
            navigate("/login");
            return;
          }

          setError(data.detail || "Failed to load notes");
          return;
        }

        setNotes(Array.isArray(data) ? data : data.notes || []);
        setTotalNotes(data.total_notes ?? 0);
        setTotalPages(Math.max(1, data.total_pages ?? 1));

      } catch (error) {
        console.error("Notes error:", error);
        setError("Unable to connect to the server.");
      } finally {
        setLoading(false);
      }
    };

    fetchNotes();
  }, [
    navigate,
    activeSection,
    currentPage,
    searchText,
    selectedTag,
    sortOrder,
  ]);


  /*
    Fetch all tags once so the Tags view does not lose tags that are
    located on another pagination page.
  */

  useEffect(() => {
    const fetchTags = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/tags"
        );

        const data = await response.json();

        if (response.ok) {
          setAllTags(data.tags || []);
        }
      } catch (error) {
        console.error("Tags error:", error);
      }
    };

    fetchTags();
  }, []);


  /*
    Fetch statistics for the logged-in user
  */

  useEffect(() => {
    if (activeSection !== "statistics") {
      return;
    }

    const fetchStats = async () => {
      const token = localStorage.getItem("token");

      if (!token) {
        navigate("/login");
        return;
      }

      try {
        const response = await fetch(
          "http://127.0.0.1:8000/stats/me",
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        const data = await response.json();

        if (!response.ok) {
          if (response.status === 401) {
            localStorage.removeItem("token");
            navigate("/login");
            return;
          }

          setError(
            data.detail ||
              "Failed to load your statistics."
          );
          return;
        }

        setStats({
          notes_count: data.notes_count ?? 0,
          unique_tags: data.unique_tags ?? 0,
          upvotes_given: data.upvotes_given ?? 0,
          comments_written: data.comments_written ?? 0,
          tag_counts: data.tag_counts ?? {},
        });
      } catch (error) {
        console.error(
          "Statistics error:",
          error
        );

        setError(
          "Unable to load your statistics."
        );
      }
    };

    fetchStats();
  }, [activeSection, navigate]);


  /*
    Notes returned by the server are already filtered, searched, sorted,
    and paginated.
  */

  const filteredNotes = notes;


  /*
    Statistics
    These values come from /stats/me and belong only to
    the currently logged-in user.
  */

  const totalComments = stats.comments_written;

  const totalUpvotes = stats.upvotes_given;

  const userTagCounts = stats.tag_counts || {};

  const userTags = Object.keys(userTagCounts).sort();


  /*
    Logout
  */

  const handleLogout = () => {
    localStorage.removeItem("token");

    setProfileOpen(false);

    navigate("/login");
  };


  /*
    Sidebar navigation
  */

  const handleSidebarClick =
    (section) => {

      setActiveSection(section);

      setSelectedTag("all");

      setSearchText("");
      setCurrentPage(1);

      setExpandedNote(null);

      setProfileOpen(false);
    };


  /*
    Fetch comments
  */

  const fetchComments =
    async (noteId) => {

      try {

        setCommentsLoading(
          (previous) => ({
            ...previous,
            [noteId]: true,
          })
        );

        const response =
          await fetch(
            `http://127.0.0.1:8000/notes/${noteId}/comments`
          );

        const data =
          await response.json();

        if (!response.ok) {

          console.error(
            "Failed to load comments:",
            data
          );

          return;
        }

        const commentsList =
          Array.isArray(data)
            ? data
            : data.comments || [];

        setComments(
          (previous) => ({
            ...previous,
            [noteId]: commentsList,
          })
        );

        setCommentCounts(
          (previous) => ({
            ...previous,
            [noteId]: commentsList.length,
          })
        );

      } catch (error) {

        console.error(
          "Comments error:",
          error
        );

      } finally {

        setCommentsLoading(
          (previous) => ({
            ...previous,
            [noteId]: false,
          })
        );
      }
    };


  /*
    Expand / collapse note
  */

  const handleNoteClick =
    (noteId) => {

      if (
        editingNote === noteId
      ) {
        return;
      }

      if (
        expandedNote === noteId
      ) {

        setExpandedNote(null);

        return;
      }

      setExpandedNote(noteId);

      fetchComments(noteId);
    };


  /*
    Upvote
  */

  const handleUpvote =
    async (
      event,
      noteId
    ) => {

      event.stopPropagation();

      const token =
        localStorage.getItem("token");

      if (!token) {
        navigate("/login");
        return;
      }

      const alreadyUpvoted =
        upvotedNotes[noteId];

      try {

        const response =
          await fetch(
            `http://127.0.0.1:8000/notes/${noteId}/upvote`,
            {
              method:
                alreadyUpvoted
                  ? "DELETE"
                  : "POST",

              headers: {
                Authorization:
                  `Bearer ${token}`,
              },
            }
          );

        const data =
          await response.json();

        if (!response.ok) {
          if (response.status === 401) {
            localStorage.removeItem("token");
            navigate("/login");
            return;
          }

          const errorMessage =
            typeof data.detail === "string"
              ? data.detail
              : "Unable to update your upvote. Please try again.";

          if (
            !alreadyUpvoted &&
            errorMessage.toLowerCase().includes("already upvoted")
          ) {
            setUpvotedNotes((previous) => ({
              ...previous,
              [noteId]: true,
            }));
            setUpvoteErrors((previous) => ({
              ...previous,
              [noteId]: "",
            }));
            return;
          }

          setError(errorMessage);

          return;
        }

        setUpvotedNotes(
          (previous) => ({
            ...previous,
            [noteId]: !alreadyUpvoted,
          })
        );

        setError("");

        setNotes(
          (previousNotes) =>
            previousNotes.map(
              (note) => {

                const currentId =
                  getNoteId(note);

                if (
                  currentId !==
                  noteId
                ) {
                  return note;
                }

                const currentCount =
                  note.upvotes_count ??
                  note.upvote_count ??
                  note.upvotes ??
                  0;

                return {
                  ...note,

                  upvotes_count:
                    alreadyUpvoted
                      ? Math.max(
                          0,
                          currentCount - 1
                        )
                      : currentCount + 1,
                };
              }
            )
        );

      } catch (error) {
        console.error("Upvote error:", error);

        setUpvoteErrors((previous) => ({
          ...previous,
          [noteId]:
            "Unable to connect to the server. Please try again.",
        }));
      }
    };


  /*
    Add comment
  */

  const handleCommentSubmit =
    async (
      event,
      noteId
    ) => {

      event.preventDefault();
      event.stopPropagation();

      const token =
        localStorage.getItem("token");

      const text =
        commentText[noteId]?.trim();

      if (!token) {
        navigate("/login");
        return;
      }

      if (!text) {
        setCommentErrors((previous) => ({
          ...previous,
          [noteId]: "Please write a comment before posting.",
        }));
        return;
      }

      setCommentErrors((previous) => ({
        ...previous,
        [noteId]: "",
      }));

      setCommentSubmitting((previous) => ({
        ...previous,
        [noteId]: true,
      }));

      try {
        const response =
          await fetch(
            `http://127.0.0.1:8000/notes/${noteId}/comments`,
            {
              method: "POST",

              headers: {
                "Content-Type":
                  "application/json",

                Authorization:
                  `Bearer ${token}`,
              },

              body: JSON.stringify({
                content: text,
              }),
            }
          );

        const data =
          await response.json();

        if (!response.ok) {
          if (response.status === 401) {
            localStorage.removeItem("token");
            navigate("/login");
            return;
          }

          setCommentErrors((previous) => ({
            ...previous,
            [noteId]:
              data.detail ||
              "Unable to add your comment. Please try again.",
          }));

          return;
        }

        const newComment =
          data?.comment ||
          data;

        setCommentText(
          (previous) => ({
            ...previous,
            [noteId]: "",
          })
        );

        if (
          newComment &&
          typeof newComment === "object" &&
          (newComment.content || newComment.text)
        ) {
          setComments((previous) => ({
            ...previous,
            [noteId]: [
              ...(previous[noteId] || []),
              newComment,
            ],
          }));

          setCommentCounts((previous) => ({
            ...previous,
            [noteId]:
              (previous[noteId] || 0) + 1,
          }));
        } else {
          await fetchComments(noteId);
        }

      } catch (error) {
        console.error("Comment error:", error);

        setCommentErrors((previous) => ({
          ...previous,
          [noteId]:
            "Unable to connect to the server. Please try again.",
        }));
      } finally {
        setCommentSubmitting((previous) => ({
          ...previous,
          [noteId]: false,
        }));
      }
    };


  /*
    Delete comment (admin moderation)
  */

  const handleDeleteComment =
    async (
      event,
      noteId,
      commentId
    ) => {

      event.stopPropagation();

      const token =
        localStorage.getItem("token");

      if (!token) {
        navigate("/login");
        return;
      }

      const confirmed =
        window.confirm(
          "Remove this comment? This action cannot be undone."
        );

      if (!confirmed) {
        return;
      }

      try {
        const response =
          await fetch(
            `http://127.0.0.1:8000/comments/${commentId}`,
            {
              method: "DELETE",
              headers: {
                Authorization:
                  `Bearer ${token}`,
              },
            }
          );

        const data =
          await response.json();

        if (!response.ok) {
          if (response.status === 401) {
            localStorage.removeItem("token");
            navigate("/login");
            return;
          }

          setCommentErrors((previous) => ({
            ...previous,
            [noteId]:
              data.detail ||
              "Unable to remove this comment.",
          }));

          return;
        }

        setComments((previous) => ({
          ...previous,
          [noteId]: (
            previous[noteId] || []
          ).filter(
            (comment) =>
              String(
                comment.id ||
                comment._id
              ) !== String(commentId)
          ),
        }));

        setCommentCounts((previous) => ({
          ...previous,
          [noteId]: Math.max(
            0,
            (previous[noteId] || 0) - 1
          ),
        }));

        setCommentErrors((previous) => ({
          ...previous,
          [noteId]: "",
        }));

      } catch (error) {
        console.error(
          "Delete comment error:",
          error
        );

        setCommentErrors((previous) => ({
          ...previous,
          [noteId]:
            "Unable to connect to the server. Please try again.",
        }));
      }
    };



  /*
    Edit note
  */

  const handleEditClick =
    (
      event,
      note
    ) => {

      event.stopPropagation();

      const noteId =
        getNoteId(note);

      setEditingNote(noteId);

      setExpandedNote(noteId);

      setEditTitle(
        note.title || ""
      );

      setEditContent(
        note.content || ""
      );

      setEditTags(
        Array.isArray(note.tags)
          ? note.tags.join(", ")
          : ""
      );
    };


  const handleCancelEdit =
    (event) => {

      event.stopPropagation();

      setEditingNote(null);
    };


  /*
    Save edited note
  */

  const handleSaveEdit =
    async (
      event,
      noteId
    ) => {

      event.preventDefault();

      event.stopPropagation();

      const token =
        localStorage.getItem("token");

      if (!token) {
        navigate("/login");
        return;
      }

      setSavingEdit(true);

      setError("");

      try {

        const tagsArray =
          editTags
            .split(",")
            .map(
              (tag) =>
                tag.trim()
            )
            .filter(
              (tag) =>
                tag !== ""
            );


        const response =
          await fetch(
            `http://127.0.0.1:8000/notes/${noteId}`,
            {
              method: "PUT",

              headers: {
                "Content-Type":
                  "application/json",

                Authorization:
                  `Bearer ${token}`,
              },

              body: JSON.stringify({
                title: editTitle,
                content: editContent,
                tags: tagsArray,
              }),
            }
          );


        const data =
          await response.json();


        if (!response.ok) {

          setError(
            data.detail ||
              "Failed to update note"
          );

          return;
        }


        setNotes(
          (previousNotes) =>
            previousNotes.map(
              (note) => {

                const currentId =
                  getNoteId(note);

                if (
                  currentId !==
                  noteId
                ) {
                  return note;
                }

                return {
                  ...note,
                  title:
                    editTitle,
                  content:
                    editContent,
                  tags:
                    tagsArray,
                };
              }
            )
        );


        setEditingNote(null);

      } catch (error) {

        console.error(
          "Update note error:",
          error
        );

        setError(
          "Unable to connect to the server."
        );

      } finally {

        setSavingEdit(false);
      }
    };


  /*
    Delete note
  */

  const handleDelete =
    async (
      event,
      noteId
    ) => {

      event.stopPropagation();

      const token =
        localStorage.getItem("token");

      if (!token) {
        navigate("/login");
        return;
      }

      const confirmed =
        window.confirm(
          "Are you sure you want to delete this note?"
        );

      if (!confirmed) {
        return;
      }

      try {

        const response =
          await fetch(
            `http://127.0.0.1:8000/notes/${noteId}`,
            {
              method: "DELETE",

              headers: {
                Authorization:
                  `Bearer ${token}`,
              },
            }
          );


        const data =
          await response.json();


        if (!response.ok) {

          setError(
            data.detail ||
              "Failed to delete note"
          );

          return;
        }


        setNotes(
          (previousNotes) =>
            previousNotes.filter(
              (note) =>
                getNoteId(note) !==
                noteId
            )
        );

        setTotalNotes((previous) => Math.max(0, previous - 1));

        setCurrentPage((page) => {
          if (notes.length === 1 && page > 1) {
            return page - 1;
          }
          return page;
        });

        setExpandedNote(null);

        setEditingNote(null);

      } catch (error) {

        console.error(
          "Delete note error:",
          error
        );

        setError(
          "Unable to connect to the server."
        );
      }
    };


  /*
    Loading screen
  */

  if (loading) {

    return (
      <div className="loading-screen">

        <div className="loading-logo">

          <Icon
            name="leaf"
            size={30}
          />

          NoteFlow

        </div>

        <p>
          Loading your notes...
        </p>

      </div>
    );
  }


  /*
    SETTINGS PAGE
    Admin only.
  */

  if (activeSection === "settings") {
    return (
      <SettingsPage
        currentUser={currentUser}
        darkMode={darkMode}
        onToggleDarkMode={() =>
          setDarkMode((previous) => !previous)
        }
        sidebarCollapsed={sidebarCollapsed}
        onToggleSidebar={() =>
          setSidebarCollapsed((previous) => !previous)
        }
        onNavigate={handleSidebarClick}
        profileOpen={profileOpen}
        onToggleProfile={() =>
          setProfileOpen((previous) => !previous)
        }
        onLogout={handleLogout}
      />
    );
  }


  /*
    STATISTICS PAGE
  */

  if (
    activeSection ===
    "statistics"
  ) {

    return (
      <div className={`dashboard ${sidebarCollapsed ? "sidebar-collapsed" : ""} ${darkMode ? "theme-dark" : ""}`}>

              <Sidebar
        activeSection={activeSection}
        sidebarCollapsed={sidebarCollapsed}
        onToggle={() => setSidebarCollapsed((previous) => !previous)}
        onNavigate={handleSidebarClick}
        isAdmin={currentUser.role === "admin"}
      />


        <div className="main-area">

          <header className="topbar">

            <div className="search-wrapper">

              <Icon
                name="search"
                size={19}
              />

              <input
                type="text"
                placeholder="Search notes..."
                value={searchText}
                onChange={(event) => {
                  setSearchText(event.target.value);
                  setCurrentPage(1);
                }}
              />

            </div>


            <div className="topbar-actions">

              <Link
                to="/create-note"
                className="create-note-button"
              >

                <Icon
                  name="plus"
                  size={19}
                />

                <span>
                  Create Note
                </span>

              </Link>


              <div className="topbar-divider" />

            <ProfileMenu
              currentUser={currentUser}
              profileOpen={profileOpen}
              onToggle={() =>
                setProfileOpen((previous) => !previous)
              }
              onNavigate={handleSidebarClick}
              onLogout={handleLogout}
            />

          </div>

        </header>


          <main className="notes-content">

            <div className="page-heading">

              <div>

                <p className="eyebrow">
                  YOUR ACTIVITY
                </p>

                <h2>
                  Statistics
                </h2>

                <p className="page-description">
                  A quick look at your
                  NoteFlow activity.
                </p>

              </div>

            </div>


            <div className="statistics-grid">

              <div className="stat-card">

                <div className="stat-card-icon">
                  <Icon
                    name="notes"
                    size={22}
                  />
                </div>

                <span>
                  Total Notes
                </span>

                <strong>
                  {stats.notes_count}
                </strong>

              </div>


              <div className="stat-card">

                <div className="stat-card-icon">
                  <Icon
                    name="tag"
                    size={22}
                  />
                </div>

                <span>
                  Unique Tags
                </span>

                <strong>
                  {stats.unique_tags}
                </strong>

              </div>


              <div className="stat-card">

                <div className="stat-card-icon">
                  <Icon
                    name="thumb"
                    size={22}
                  />
                </div>

                <span>
                  Upvotes Given
                </span>

                <strong>
                  {totalUpvotes}
                </strong>

              </div>


              <div className="stat-card">

                <div className="stat-card-icon">
                  <Icon
                    name="comment"
                    size={22}
                  />
                </div>

                <span>
                  Comments Written
                </span>

                <strong>
                  {totalComments}
                </strong>

              </div>

            </div>


            <div className="statistics-panel">

              <div className="statistics-panel-heading">

                <h3>
                  Your tags
                </h3>

                <span>
                  {stats.unique_tags} tags
                </span>

              </div>


              {userTags.length === 0 ? (
                <p className="muted-text">
                  No tags have been added to your notes yet.
                </p>
              ) : (
                <div className="statistics-tags">
                  {userTags.map((tag) => (
                    <div
                      className="statistics-tag"
                      key={tag}
                    >
                      <span>
                        {tag}
                      </span>

                      <strong>
                        {userTagCounts[tag]}
                      </strong>
                    </div>
                  ))}
                </div>
              )}

            </div>


            <button
              className="back-to-notes"
              onClick={() =>
                handleSidebarClick(
                  "all"
                )
              }
            >
              ← Back to all notes
            </button>

          </main>

        </div>

      </div>
    );
  }


  /*
    MAIN NOTES PAGE
  */

  return (
    <div className={`dashboard ${sidebarCollapsed ? "sidebar-collapsed" : ""} ${darkMode ? "theme-dark" : ""}`}>

      {/* SIDEBAR */}

              <Sidebar
          activeSection={activeSection}
          sidebarCollapsed={sidebarCollapsed}
          onToggle={() => setSidebarCollapsed((previous) => !previous)}
          onNavigate={handleSidebarClick}
          isAdmin={currentUser.role === "admin"}
        />


      {/* MAIN AREA */}

      <div className="main-area">

        {/* TOP BAR */}

        <header className="topbar">

          <div className="search-wrapper">

            <Icon
              name="search"
              size={19}
            />

            <input
              type="text"
              placeholder="Search notes by title, content or tags..."
              value={searchText}
              onChange={(event) => {
                setSearchText(event.target.value);
                setCurrentPage(1);
              }}
            />

            <span className="search-shortcut">
              /
            </span>

          </div>


          <div className="topbar-actions">

            <Link
              to="/create-note"
              className="create-note-button"
            >

              <Icon
                name="plus"
                size={19}
              />

              <span>
                Create Note
              </span>

            </Link>


            <div className="topbar-divider" />


            {/* PROFILE */}

            <ProfileMenu
              currentUser={currentUser}
              profileOpen={profileOpen}
              onToggle={() =>
                setProfileOpen((previous) => !previous)
              }
              onNavigate={handleSidebarClick}
              onLogout={handleLogout}
            />

          </div>

        </header>


        {/* PAGE CONTENT */}

        <main className="notes-content">

          <div className="page-heading">

            <div>

              <p className="eyebrow">

                {activeSection === "my"
                  ? "YOUR NOTES"
                  : activeSection === "tags"
                  ? "ORGANIZE"
                  : "YOUR WORKSPACE"}

              </p>


              <h2>

                {activeSection === "my"
                  ? "My Notes"
                  : activeSection === "tags"
                  ? "Tags"
                  : "All Notes"}

              </h2>


              <p className="page-description">

                {activeSection === "my"
                  ? "Notes created by you."
                  : activeSection === "tags"
                  ? "Browse your notes by topic."
                  : "Capture your ideas, learnings and thoughts — all in one place."}

              </p>

            </div>


            <div className="note-count">

              <strong>
                {totalNotes}
              </strong>

              <span>
                {totalNotes === 1
                  ? "note"
                  : "notes"}
              </span>

            </div>

          </div>


          {/* TAG VIEW */}

          {activeSection === "tags" && (

            <div className="tag-selector">

              <button
                className={
                  selectedTag === "all"
                    ? "tag-filter active"
                    : "tag-filter"
                }
                onClick={() => {
                  setSelectedTag("all");
                  setCurrentPage(1);
                }}
              >
                All
              </button>


              {allTags.map(
                (tag) => (

                  <button
                    key={tag}
                    className={
                      selectedTag ===
                      tag
                        ? "tag-filter active"
                        : "tag-filter"
                    }
                    onClick={() => {
                      setSelectedTag(tag);
                      setCurrentPage(1);
                    }}
                  >
                    {tag}
                  </button>

                )
              )}

            </div>

          )}


          {/* FILTER BAR */}

          {activeSection !== "tags" && (

            <div className="filter-bar">

              <button
                className="filter-button"
                onClick={() =>
                  handleSidebarClick(
                    "tags"
                  )
                }
              >

                <Icon
                  name="tag"
                  size={17}
                />

                <span>
                  Browse Tags
                </span>

                <Icon
                  name="arrow"
                  size={15}
                />

              </button>


              {/* SORT DROPDOWN */}

              <div className="sort-container">

                <button
                  className="filter-button"
                  onClick={() =>
                    document
                      .getElementById(
                        "sort-menu"
                      )
                      ?.classList.toggle(
                        "show"
                      )
                  }
                >

                  <Icon
                    name="sort"
                    size={17}
                  />

                  <span>
                    {sortOrder ===
                    "newest"
                      ? "Newest First"
                      : sortOrder ===
                        "oldest"
                      ? "Oldest First"
                      : "Most Popular"}
                  </span>

                  <Icon
                    name="arrow"
                    size={15}
                  />

                </button>


                <div
                  id="sort-menu"
                  className="sort-menu"
                >

                  <button
                    className={
                      sortOrder ===
                      "newest"
                        ? "sort-option selected"
                        : "sort-option"
                    }
                    onClick={() => {

                      setSortOrder(
                        "newest"
                      );
                      setCurrentPage(1);

                      document
                        .getElementById(
                          "sort-menu"
                        )
                        ?.classList.remove(
                          "show"
                        );

                    }}
                  >

                    <span>
                      Newest First
                    </span>

                    {sortOrder ===
                      "newest" && (
                      <span>✓</span>
                    )}

                  </button>


                  <button
                    className={
                      sortOrder ===
                      "oldest"
                        ? "sort-option selected"
                        : "sort-option"
                    }
                    onClick={() => {

                      setSortOrder(
                        "oldest"
                      );
                      setCurrentPage(1);

                      document
                        .getElementById(
                          "sort-menu"
                        )
                        ?.classList.remove(
                          "show"
                        );

                    }}
                  >

                    <span>
                      Oldest First
                    </span>

                    {sortOrder ===
                      "oldest" && (
                      <span>✓</span>
                    )}

                  </button>


                  <button
                    className={
                      sortOrder ===
                      "popular"
                        ? "sort-option selected"
                        : "sort-option"
                    }
                    onClick={() => {

                      setSortOrder(
                        "popular"
                      );
                      setCurrentPage(1);

                      document
                        .getElementById(
                          "sort-menu"
                        )
                        ?.classList.remove(
                          "show"
                        );

                    }}
                  >

                    <span>
                      Most Popular
                    </span>

                    {sortOrder ===
                      "popular" && (
                      <span>✓</span>
                    )}

                  </button>

                </div>

              </div>

            </div>

          )}


          {error && (

            <div className="dashboard-error">
              {error}
            </div>

          )}


          {/* NOTES */}

          {filteredNotes.length === 0 ? (

            <div className="empty-state">

              <div className="empty-icon">

                <Icon
                  name="notes"
                  size={30}
                />

              </div>


              <h3>

                {searchText
                  ? "No matching notes"
                  : activeSection ===
                    "my"
                  ? "You haven't created any notes yet"
                  : selectedTag !==
                    "all"
                  ? "No notes with this tag"
                  : "No notes yet"}

              </h3>


              <p>

                {searchText
                  ? "Try a different search term."
                  : "Create your first note and start building your knowledge base."}

              </p>


              {!searchText && (

                <Link
                  to="/create-note"
                  className="create-note-button empty-button"
                >

                  <Icon
                    name="plus"
                    size={18}
                  />

                  Create your first note

                </Link>

              )}

            </div>

          ) : (

            <div className="notes-grid">

              {filteredNotes.map(
                (
                  note,
                  index
                ) => {

                  const noteId =
                    getNoteId(note);

                  const isExpanded =
                    expandedNote ===
                    noteId;

                  const isEditing =
                    editingNote ===
                    noteId;

                  const upvoteCount =
                    note.upvotes_count ??
                    note.upvote_count ??
                    note.upvotes ??
                    0;

                  const noteComments =
                    comments[
                      noteId
                    ] || [];

                  const cardColor =
                    `note-color-${
                      (index % 5) + 1
                    }`;


                  return (

                    <article
                      className={`dashboard-note-card ${cardColor} ${
                        isExpanded
                          ? "expanded"
                          : ""
                      }`}
                      key={noteId}
                    >

                      <div
                        className="note-click-area"
                        onClick={() =>
                          handleNoteClick(
                            noteId
                          )
                        }
                      >

                        {!isEditing ? (

                          <>

                            <div className="note-tags-row">

                              {Array.isArray(
                                note.tags
                              ) &&
                              note.tags
                                .length >
                                0 ? (

                                note.tags
                                  .slice(
                                    0,
                                    3
                                  )
                                  .map(
                                    (
                                      tag
                                    ) => (

                                      <span
                                        className="tag-pill"
                                        key={
                                          tag
                                        }
                                      >
                                        {tag}
                                      </span>

                                    )
                                  )

                              ) : (

                                <span className="tag-pill neutral">
                                  note
                                </span>

                              )}

                            </div>


                            <h3 className="note-title">
                              {note.title}
                            </h3>


                            <div
                              className={
                                isExpanded
                                  ? "note-full-content"
                                  : "note-preview"
                              }
                            >
                              {note.content}
                            </div>


                            {isExpanded &&
                              note.tags &&
                              note.tags.length >
                                0 && (

                                <div className="expanded-tags">

                                  {note.tags.map(
                                    (
                                      tag
                                    ) => (

                                      <span
                                        className="tag-pill"
                                        key={
                                          tag
                                        }
                                      >
                                        {tag}
                                      </span>

                                    )
                                  )}

                                </div>

                              )}

                          </>

                        ) : (

                          <form
                            className="edit-note-form"
                            onSubmit={(
                              event
                            ) =>
                              handleSaveEdit(
                                event,
                                noteId
                              )
                            }
                          >

                            <div className="form-group">

                              <label>
                                Title
                              </label>

                              <input
                                type="text"
                                value={
                                  editTitle
                                }
                                onChange={(
                                  event
                                ) =>
                                  setEditTitle(
                                    event
                                      .target
                                      .value
                                  )
                                }
                                required
                              />

                            </div>


                            <div className="form-group">

                              <label>
                                Content
                              </label>

                              <textarea
                                value={
                                  editContent
                                }
                                onChange={(
                                  event
                                ) =>
                                  setEditContent(
                                    event
                                      .target
                                      .value
                                  )
                                }
                                rows="8"
                                required
                              />

                            </div>


                            <div className="form-group">

                              <label>
                                Tags
                              </label>

                              <input
                                type="text"
                                value={
                                  editTags
                                }
                                onChange={(
                                  event
                                ) =>
                                  setEditTags(
                                    event
                                      .target
                                      .value
                                  )
                                }
                                placeholder="react, database"
                              />

                            </div>


                            <div className="edit-buttons">

                              <button
                                type="submit"
                                disabled={
                                  savingEdit
                                }
                              >
                                {savingEdit
                                  ? "Saving..."
                                  : "Save Changes"}
                              </button>


                              <button
                                type="button"
                                onClick={
                                  handleCancelEdit
                                }
                              >
                                Cancel
                              </button>

                            </div>

                          </form>

                        )}

                      </div>


                      {!isEditing && (

                        <div className="note-card-footer">

                          <div className="note-date">

                            <Icon
                              name="calendar"
                              size={15}
                            />

                            <span>
                              {formatDate(
                                note.created_at ||
                                  note.createdAt ||
                                  note.updated_at
                              )}
                            </span>

                          </div>


                          <div className="note-stat">

                            <Icon
                              name="comment"
                              size={15}
                            />

                            <span>
                              {
                                commentCounts[noteId] ??
                                note.comment_count ??
                                note.comments_count ??
                                noteComments.length
                              }
                            </span>

                          </div>


                          <button
                            className={
                              upvotedNotes[
                                noteId
                              ]
                                ? "note-stat action-stat upvoted"
                                : "note-stat action-stat"
                            }
                            onClick={(
                              event
                            ) =>
                              handleUpvote(
                                event,
                                noteId
                              )
                            }
                          >

                            <Icon
                              name="thumb"
                              size={15}
                            />

                            <span>
                              {upvotedNotes[noteId]
                                ? "Upvoted"
                                : "Upvote"}
                              {" "}
                              {upvoteCount}
                            </span>

                          </button>


                          {isExpanded && (

                            <div className="note-card-actions">

                              <button
                                className="card-action edit-action"
                                onClick={(
                                  event
                                ) =>
                                  handleEditClick(
                                    event,
                                    note
                                  )
                                }
                              >
                                Edit
                              </button>


                              <button
                                className="card-action delete-action"
                                onClick={(
                                  event
                                ) =>
                                  handleDelete(
                                    event,
                                    noteId
                                  )
                                }
                              >
                                Delete
                              </button>

                            </div>

                          )}


                          {!isExpanded && (

                            <span className="more-icon">

                              <Icon
                                name="more"
                                size={18}
                              />

                            </span>

                          )}

                        </div>

                      )}


                      {isExpanded &&
                        !isEditing && (

                          <div className="expanded-section">

                            <div className="expanded-divider" />


                            <div className="comments-section">

                              <div className="comments-heading">

                                <h4>
                                  Comments
                                </h4>

                                <span>
                                  {
                                    commentCounts[noteId] ??
                                    noteComments.length
                                  }
                                </span>

                              </div>


                              {commentsLoading[
                                noteId
                              ] ? (

                                <p className="muted-text">
                                  Loading comments...
                                </p>

                              ) : noteComments.length ===
                                0 ? (

                                <p className="muted-text">
                                  No comments yet.
                                  Be the first
                                  to share your
                                  thoughts.
                                </p>

                              ) : (

                                <div className="comments-list">

                                  {noteComments.map(
                                    (
                                      comment
                                    ) => (

                                      <div
                                        className="comment"
                                        key={
                                          comment.id ||
                                          comment._id
                                        }
                                      >

                                        <div className="comment-avatar">

                                          {(
                                            comment.username ||
                                            comment.user ||
                                            "U"
                                          )
                                            .charAt(
                                              0
                                            )
                                            .toUpperCase()}

                                        </div>


                                        <div className="comment-body">

                                          <strong>
                                            {
                                              comment.username ||
                                              comment.user ||
                                              "User"
                                            }
                                          </strong>

                                          <p>
                                            {
                                              comment.content ||
                                              comment.text
                                            }
                                          </p>

                                          {currentUser.role === "admin" && (
                                            <button
                                              type="button"
                                              className="comment-delete-button"
                                              onClick={(event) =>
                                                handleDeleteComment(
                                                  event,
                                                  noteId,
                                                  comment.id ||
                                                    comment._id
                                                )
                                              }
                                              aria-label="Delete comment"
                                              title="Delete comment"
                                            >
                                              <Icon name="trash" size={15} />
                                            </button>
                                          )}

                                        </div>

                                      </div>

                                    )
                                  )}

                                </div>

                              )}


                              {commentErrors[noteId] && (
                                <div className="comment-error">
                                  {commentErrors[noteId]}
                                </div>
                              )}

                              <form
                                className="comment-form"
                                onSubmit={(
                                  event
                                ) =>
                                  handleCommentSubmit(
                                    event,
                                    noteId
                                  )
                                }
                              >

                                <input
                                  type="text"
                                  placeholder="Write a comment..."
                                  value={
                                    commentText[
                                      noteId
                                    ] || ""
                                  }
                                  onChange={(
                                    event
                                  ) =>
                                    setCommentText(
                                      (
                                        previous
                                      ) => ({
                                        ...previous,
                                        [noteId]:
                                          event
                                            .target
                                            .value,
                                      })
                                    )
                                  }
                                />


                                <button
                                  type="submit"
                                  disabled={
                                    commentSubmitting[noteId]
                                  }
                                >
                                  {commentSubmitting[noteId]
                                    ? "Posting..."
                                    : "Comment"}
                                </button>

                              </form>

                            </div>


                            <button
                              className="collapse-button"
                              onClick={() =>
                                setExpandedNote(
                                  null
                                )
                              }
                            >
                              Collapse note
                            </button>

                          </div>

                        )}

                    </article>

                  );
                }
              )}

            </div>

          )}


          {totalPages > 1 && (
            <div className="pagination" aria-label="Notes pagination">
              <button
                type="button"
                className="pagination-button pagination-arrow"
                onClick={() =>
                  setCurrentPage((page) => Math.max(1, page - 1))
                }
                disabled={currentPage === 1}
                aria-label="Previous page"
              >
                <Icon name="arrow" size={16} />
              </button>

              {Array.from(
                { length: totalPages },
                (_, index) => index + 1
              ).map((page) => (
                <button
                  type="button"
                  key={page}
                  className={
                    page === currentPage
                      ? "pagination-button active"
                      : "pagination-button"
                  }
                  onClick={() => setCurrentPage(page)}
                  aria-current={
                    page === currentPage ? "page" : undefined
                  }
                >
                  {page}
                </button>
              ))}

              <button
                type="button"
                className="pagination-button pagination-arrow next"
                onClick={() =>
                  setCurrentPage((page) =>
                    Math.min(totalPages, page + 1)
                  )
                }
                disabled={currentPage === totalPages}
                aria-label="Next page"
              >
                <Icon name="arrow" size={16} />
              </button>
            </div>
          )}


          {notes.length > 0 &&
            !searchText && (

              <div className="bottom-quote">

                <p>
                  “Small notes,
                  <br />
                  big progress.”
                </p>

                <span />

              </div>

            )}

        </main>

      </div>

    </div>
  );
}

export default Notes;