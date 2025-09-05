// Firebase configuration - Fetched from backend
let firebaseConfig = null;
let auth = null;
let googleProvider = null;

// Initialize Firebase with config from backend
async function initializeFirebase() {
  try {
    const response = await fetch("/api/firebase-config");
    firebaseConfig = await response.json();

    // Initialize Firebase
    firebase.initializeApp(firebaseConfig);
    auth = firebase.auth();
    googleProvider = new firebase.auth.GoogleAuthProvider();

    console.log("Firebase initialized successfully");
  } catch (error) {
    console.error("Failed to initialize Firebase:", error);
    alert("Failed to initialize Firebase. Please refresh the page.");
  }
}

function showLoading() {
  document.getElementById("loading-overlay").style.display = "flex";
}

function hideLoading() {
  document.getElementById("loading-overlay").style.display = "none";
}

function handleAuthSuccess(user) {
  showLoading();
  user
    .getIdToken()
    .then(function (idToken) {
      fetch("/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          idToken: idToken,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          hideLoading();
          if (data.success) {
            window.location.href = data.redirect;
          } else {
            alert("Authentication failed: " + data.error);
          }
        })
        .catch((error) => {
          hideLoading();
          console.error("Error:", error);
          alert("An error occurred during authentication");
        });
    })
    .catch(function (error) {
      hideLoading();
      console.error("Error getting ID token:", error);
      alert("Failed to get authentication token");
    });
}

// Initialize event listeners when DOM is loaded
document.addEventListener("DOMContentLoaded", async function () {
  // Initialize Firebase first
  await initializeFirebase();

  // Check if Firebase was initialized successfully
  if (!auth) {
    alert("Firebase initialization failed. Please refresh the page.");
    return;
  }
  // Get Started button (Email/Password Sign In)
  document
    .getElementById("get-started-btn")
    .addEventListener("click", function () {
      const email = document.getElementById("firebase-email").value;
      const password = document.getElementById("firebase-password").value;

      if (!email || !password) {
        alert("Please enter both email and password");
        return;
      }

      showLoading();

      // Try to sign in first, if it fails, offer to sign up
      auth
        .signInWithEmailAndPassword(email, password)
        .then(function (result) {
          handleAuthSuccess(result.user);
        })
        .catch(function (error) {
          if (error.code === "auth/user-not-found") {
            // User doesn't exist, ask if they want to create an account
            if (
              confirm(
                "No account found with this email. Would you like to create a new account?"
              )
            ) {
              if (password.length < 6) {
                hideLoading();
                alert("Password must be at least 6 characters long");
                return;
              }
              auth
                .createUserWithEmailAndPassword(email, password)
                .then(function (result) {
                  handleAuthSuccess(result.user);
                })
                .catch(function (signupError) {
                  hideLoading();
                  alert("Sign-up failed: " + signupError.message);
                });
            } else {
              hideLoading();
            }
          } else {
            hideLoading();
            alert("Sign-in failed: " + error.message);
          }
        });
    });

  // Google Sign In
  document
    .getElementById("google-login-btn")
    .addEventListener("click", function () {
      showLoading();
      auth
        .signInWithPopup(googleProvider)
        .then(function (result) {
          handleAuthSuccess(result.user);
        })
        .catch(function (error) {
          hideLoading();
          console.error("Google sign-in error:", error);
          alert("Google sign-in failed: " + error.message);
        });
    });

  // Handle Enter key in form fields
  document
    .getElementById("firebase-email")
    .addEventListener("keypress", function (e) {
      if (e.key === "Enter") {
        document.getElementById("firebase-password").focus();
      }
    });

  document
    .getElementById("firebase-password")
    .addEventListener("keypress", function (e) {
      if (e.key === "Enter") {
        document.getElementById("get-started-btn").click();
      }
    });

  // Sign up link functionality
  document
    .getElementById("signup-link")
    .addEventListener("click", function (e) {
      e.preventDefault();
      const email = document.getElementById("firebase-email").value;
      const password = document.getElementById("firebase-password").value;

      if (!email || !password) {
        alert("Please enter email and password to create an account");
        return;
      }

      if (password.length < 6) {
        alert("Password must be at least 6 characters long");
        return;
      }

      showLoading();
      auth
        .createUserWithEmailAndPassword(email, password)
        .then(function (result) {
          handleAuthSuccess(result.user);
        })
        .catch(function (error) {
          hideLoading();
          alert("Sign-up failed: " + error.message);
        });
    });
});
