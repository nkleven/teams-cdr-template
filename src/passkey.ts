export async function setupFirstRunExperience() {
  await showLoginModal();
}

async function showLoginModal() {
  const modal = document.createElement('div');
  modal.style.position = 'fixed';
  modal.style.top = '0';
  modal.style.left = '0';
  modal.style.width = '100%';
  modal.style.height = '100%';
  modal.style.backgroundColor = 'rgba(0,0,0,0.4)';
  modal.style.display = 'flex';
  modal.style.justifyContent = 'center';
  modal.style.alignItems = 'center';
  modal.style.zIndex = '1000';
  modal.style.backdropFilter = 'blur(4px)';

  const content = document.createElement('div');
  content.style.backgroundColor = '#fff';
  content.style.padding = '44px';
  content.style.width = '500px';
  content.style.boxShadow = '0 2px 6px rgba(0,0,0,0.2)';
  content.style.textAlign = 'center';
  content.style.fontFamily = '"Segoe UI", "Helvetica Neue", "Lucida Grande", "Roboto", "Ebrima", "Nirmala UI", "Gadugi", "Segoe Xbox Symbol", "Segoe UI Symbol", "Meiryo UI", "Khmer UI", "Tunga", "Lao UI", "Raavi", "Iskoola Pota", "Latha", "Leelawadee", "Microsoft YaHei UI", "Microsoft JhengHei UI", "Malgun Gothic", "Estrangelo Edessa", "Microsoft Himalaya", "Microsoft New Tai Lue", "Microsoft PhagsPa", "Microsoft Tai Le", "Microsoft Yi Baiti", "Mongolian Baiti", "MV Boli", "Myanmar Text", "Cambria Math"';
  content.style.color = '#1b1b1b';

  const hasPasskey = localStorage.getItem('hasPasskey');

  content.innerHTML = `
    <h2 style="font-size: 28px; font-weight: 600; margin-bottom: 12px; margin-top: 0; color: #464775;">Welcome to CDR Dashboard</h2>
    <p style="font-size: 15px; margin-bottom: 32px; color: #605e5c;">
      ${hasPasskey ? 'Please sign in to continue' : 'Let\'s secure your account with a passkey'}
    </p>

    <div style="background-color: #f3f2f1; padding: 24px; border-radius: 4px; margin-bottom: 24px; text-align: left;">
        <h3 style="margin-top: 0; font-size: 16px; color: #323130;">🔐 Secure Authentication</h3>
        <p style="margin: 0; font-size: 14px; color: #605e5c; line-height: 1.5;">
          ${hasPasskey
            ? 'Use your passkey (fingerprint, face, or security key) to sign in securely.'
            : 'Passkeys are a safer and easier way to sign in. Use your fingerprint, face, or screen lock instead of a password.'}
        </p>
    </div>

    <div style="display: flex; flex-direction: column; gap: 12px;">
        <button id="login-btn" style="
            background-color: #6264a7;
            color: white;
            border: none;
            padding: 12px 32px;
            font-size: 15px;
            cursor: pointer;
            width: 100%;
            font-weight: 600;
            border-radius: 2px;
        ">${hasPasskey ? 'Sign in with Passkey' : 'Create Passkey'}</button>

        ${hasPasskey ? `
        <button id="create-new-btn" style="
            background-color: transparent;
            color: #6264a7;
            border: 1px solid #6264a7;
            padding: 12px 32px;
            font-size: 15px;
            cursor: pointer;
            width: 100%;
            font-weight: 600;
            border-radius: 2px;
        ">Create New Passkey</button>
        ` : ''}
    </div>
  `;

  const loginBtn = content.querySelector('#login-btn') as HTMLElement;
  loginBtn.onmouseover = () => loginBtn.style.backgroundColor = '#464775';
  loginBtn.onmouseout = () => loginBtn.style.backgroundColor = '#6264a7';

  const createNewBtn = content.querySelector('#create-new-btn') as HTMLElement;
  if (createNewBtn) {
    createNewBtn.onmouseover = () => {
      createNewBtn.style.backgroundColor = '#f3f2f1';
    };
    createNewBtn.onmouseout = () => {
      createNewBtn.style.backgroundColor = 'transparent';
    };
  }

  modal.appendChild(content);
  document.body.appendChild(modal);

  return new Promise<void>((resolve) => {
    document.getElementById('login-btn')?.addEventListener('click', async () => {
      try {
        if (hasPasskey) {
          // Login with existing passkey
          await authenticateWithPasskey();
        } else {
          // Create new passkey
          await createPasskey();
          localStorage.setItem('hasPasskey', 'true');
        }

        localStorage.setItem('isLoggedIn', 'true');
        document.body.removeChild(modal);

        // Check if setup is complete
        const isSetupComplete = localStorage.getItem('isSetupComplete');
        if (!isSetupComplete) {
          // Navigate to setup wizard
          window.location.reload();
        } else {
          // Navigate to dashboard
          window.location.reload();
        }

        resolve();
      } catch (e) {
        console.error(e);
        alert('Authentication failed. Please try again.');
      }
    });

    document.getElementById('create-new-btn')?.addEventListener('click', async () => {
      try {
        await createPasskey();
        localStorage.setItem('hasPasskey', 'true');
        localStorage.setItem('isLoggedIn', 'true');
        document.body.removeChild(modal);

        // Check if setup is complete
        const isSetupComplete = localStorage.getItem('isSetupComplete');
        if (!isSetupComplete) {
          // Navigate to setup wizard
          window.location.reload();
        } else {
          // Navigate to dashboard
          window.location.reload();
        }

        resolve();
      } catch (e) {
        console.error(e);
        alert('Passkey creation failed. Please try again.');
      }
    });
  });
}

async function createPasskey() {
  const challenge = new Uint8Array(32);
  window.crypto.getRandomValues(challenge);

  const publicKey: PublicKeyCredentialCreationOptions = {
    challenge: challenge,
    rp: {
      name: "CDR Dashboard",
      id: window.location.hostname,
    },
    user: {
      id: Uint8Array.from("cdr_user", c => c.charCodeAt(0)),
      name: "user@contoso.com",
      displayName: "CDR User",
    },
    pubKeyCredParams: [{ alg: -7, type: "public-key" }],
    authenticatorSelection: {
      authenticatorAttachment: "platform",
    },
    timeout: 60000,
    attestation: "direct"
  };

  return navigator.credentials.create({ publicKey });
}

async function authenticateWithPasskey() {
  const challenge = new Uint8Array(32);
  window.crypto.getRandomValues(challenge);

  const publicKey: PublicKeyCredentialRequestOptions = {
    challenge: challenge,
    timeout: 60000,
    rpId: window.location.hostname,
    userVerification: "required"
  };

  return navigator.credentials.get({ publicKey });
}
