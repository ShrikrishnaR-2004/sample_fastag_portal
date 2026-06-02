/**
 * FASTag Portal — main.js
 * All interactive behaviours for every page.
 * No inline scripts; pages call init functions at the bottom of their body.
 */

/* =========================================================
   UTILITY HELPERS
   ========================================================= */

/**
 * Add/remove a class based on a boolean condition.
 * @param {Element} el
 * @param {string} cls
 * @param {boolean} condition
 */
function toggleClass(el, cls, condition) {
  if (!el) return;
  if (condition) el.classList.add(cls);
  else el.classList.remove(cls);
}

/**
 * Show an element (removes 'hidden', adds 'visible' if needed).
 * @param {Element} el
 */
function show(el) {
  if (!el) return;
  el.classList.remove('hidden');
}

/**
 * Hide an element.
 * @param {Element} el
 */
function hide(el) {
  if (!el) return;
  el.classList.add('hidden');
}

/**
 * Format seconds as MM:SS.
 * @param {number} secs
 * @returns {string}
 */
function formatTime(secs) {
  const m = Math.floor(secs / 60).toString().padStart(2, '0');
  const s = (secs % 60).toString().padStart(2, '0');
  return `${m}:${s}`;
}

/* =========================================================
   PASSWORD VISIBILITY TOGGLE
   ========================================================= */

/**
 * Wire up a show/hide toggle for a password input.
 * @param {string} inputId
 * @param {string} toggleId
 */
function initPasswordToggle(inputId, toggleId) {
  const input = document.getElementById(inputId);
  const toggle = document.getElementById(toggleId);
  if (!input || !toggle) return;

  toggle.addEventListener('click', () => {
    const isPassword = input.type === 'password';
    input.type = isPassword ? 'text' : 'password';
    toggle.textContent = isPassword ? '🙈' : '👁';
    toggle.setAttribute('aria-label', isPassword ? 'Hide password' : 'Show password');
  });
}

/* =========================================================
   MOBILE NUMBER AUTO-FORMAT
   ========================================================= */

/**
 * Auto-insert a space after the 5th digit of a mobile number field.
 * @param {string} inputId
 */
function initMobileFormat(inputId) {
  const input = document.getElementById(inputId);
  if (!input) return;

  input.addEventListener('input', () => {
    let val = input.value.replace(/\D/g, '').substring(0, 10);
    if (val.length > 5) {
      val = val.slice(0, 5) + ' ' + val.slice(5);
    }
    input.value = val;
  });
}

/* =========================================================
   LOGIN PAGE
   ========================================================= */

function initLogin() {
  // Mobile format
  initMobileFormat('mobile');

  // Password toggle
  initPasswordToggle('password', 'pw-toggle');

  // Attempt counter / lockout
  let attempts = 0;
  const MAX_ATTEMPTS = 3;
  const LOCKOUT_SECONDS = 300; // 5 minutes

  const form = document.getElementById('login-form');
  const mobileInput = document.getElementById('mobile');
  const passwordInput = document.getElementById('password');
  const mobileErr = document.getElementById('mobile-error');
  const passwordErr = document.getElementById('password-error');
  const lockoutBanner = document.getElementById('lockout-banner');
  const lockoutTimer = document.getElementById('lockout-timer');
  const signInBtn = document.getElementById('sign-in-btn');

  let lockoutInterval = null;

  function showFieldError(input, msgEl, message) {
    input.classList.add('error');
    msgEl.textContent = message;
    msgEl.classList.add('visible');
  }

  function clearFieldError(input, msgEl) {
    input.classList.remove('error');
    msgEl.classList.remove('visible');
  }

  // Clear errors on input
  if (mobileInput) {
    mobileInput.addEventListener('input', () => clearFieldError(mobileInput, mobileErr));
  }
  if (passwordInput) {
    passwordInput.addEventListener('input', () => clearFieldError(passwordInput, passwordErr));
  }

  function startLockout() {
    signInBtn.disabled = true;
    lockoutBanner.classList.add('visible');
    let remaining = LOCKOUT_SECONDS;
    lockoutTimer.textContent = formatTime(remaining);

    lockoutInterval = setInterval(() => {
      remaining -= 1;
      lockoutTimer.textContent = formatTime(remaining);
      if (remaining <= 0) {
        clearInterval(lockoutInterval);
        signInBtn.disabled = false;
        lockoutBanner.classList.remove('visible');
        attempts = 0;
      }
    }, 1000);
  }

  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();

      if (signInBtn.disabled) return;

      // Simulate validation: show errors for demo
      let hasError = false;
      const mobileVal = (mobileInput ? mobileInput.value.replace(/\s/g, '') : '');
      const passwordVal = (passwordInput ? passwordInput.value : '');

      clearFieldError(mobileInput, mobileErr);
      clearFieldError(passwordInput, passwordErr);

      if (!mobileVal || mobileVal.length < 10) {
        showFieldError(mobileInput, mobileErr, 'Mobile number not found');
        hasError = true;
      }

      if (!passwordVal || passwordVal.length < 1) {
        showFieldError(passwordInput, passwordErr, 'Incorrect password');
        hasError = true;
      }

      if (hasError) {
        attempts += 1;
        if (attempts >= MAX_ATTEMPTS) {
          startLockout();
        }
      }
      // On success (all valid), allow normal form submission
    });
  }
}

/* =========================================================
   SIGNUP PAGE — STEP CARDS
   ========================================================= */

function initSignup() {
  // Step navigation
  const stepCards = document.querySelectorAll('.step-card');

  function activateStep(index) {
    stepCards.forEach((card, i) => {
      card.classList.remove('active');
      if (i < index) {
        card.classList.add('completed');
      }
    });
    if (stepCards[index]) {
      stepCards[index].classList.add('active');
      stepCards[index].classList.remove('completed');
    }
  }

  stepCards.forEach((card, i) => {
    const header = card.querySelector('.step-card-header');
    if (header) {
      header.addEventListener('click', () => {
        // Only allow clicking if already completed or active
        if (card.classList.contains('completed') || card.classList.contains('active')) {
          activateStep(i);
        }
      });
    }

    // Next button inside each step
    const nextBtn = card.querySelector('[data-next-step]');
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        card.classList.remove('active');
        card.classList.add('completed');
        if (i + 1 < stepCards.length) {
          activateStep(i + 1);
        }
      });
    }
  });

  // Activate first step
  activateStep(0);

  // Password toggles for signup
  initPasswordToggle('create-password', 'create-pw-toggle');
  initPasswordToggle('confirm-password', 'confirm-pw-toggle');

  // Mobile format in signup
  initMobileFormat('signup-phone');

  // Date of Birth age gate
  const dobInput = document.getElementById('dob');
  const dobError = document.getElementById('dob-error');
  if (dobInput && dobError) {
    dobInput.addEventListener('change', () => {
      const dob = new Date(dobInput.value);
      const today = new Date();
      let age = today.getFullYear() - dob.getFullYear();
      const m = today.getMonth() - dob.getMonth();
      if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) age--;
      if (age < 18) {
        dobError.classList.add('visible');
        dobInput.classList.add('error');
      } else {
        dobError.classList.remove('visible');
        dobInput.classList.remove('error');
      }
    });
  }

  // Aadhaar masking + formatting
  const aadhaarInput = document.getElementById('aadhaar');
  if (aadhaarInput) {
    aadhaarInput.addEventListener('input', (e) => {
      // Remove non-digits, limit to 12
      let digits = aadhaarInput.value.replace(/\D/g, '').substring(0, 12);
      // Mask all but last 4 for display
      let masked = '';
      for (let i = 0; i < digits.length; i++) {
        if (i > 0 && i % 4 === 0) masked += ' ';
        masked += (i < digits.length - 4) ? '•' : digits[i];
      }
      // Store raw digits in data attribute
      aadhaarInput.dataset.rawValue = digits;
      aadhaarInput.value = masked;
    });
    // Prevent cursor confusion — use keydown to handle digit keys
    aadhaarInput.addEventListener('keydown', (e) => {
      if (e.key === 'Backspace') {
        const raw = (aadhaarInput.dataset.rawValue || '');
        aadhaarInput.dataset.rawValue = raw.slice(0, -1);
        // Trigger input event to reformat
        aadhaarInput.dispatchEvent(new Event('input'));
        e.preventDefault();
      } else if (/^\d$/.test(e.key)) {
        const raw = (aadhaarInput.dataset.rawValue || '');
        if (raw.length < 12) {
          aadhaarInput.dataset.rawValue = raw + e.key;
          aadhaarInput.dispatchEvent(new Event('input'));
        }
        e.preventDefault();
      }
    });
  }

  // PAN validation
  const panInput = document.getElementById('pan');
  const panTick = document.getElementById('pan-tick');
  const panPattern = /^[A-Z]{5}[0-9]{4}[A-Z]{1}$/;
  if (panInput) {
    panInput.addEventListener('input', () => {
      panInput.value = panInput.value.toUpperCase().replace(/[^A-Z0-9]/g, '').substring(0, 10);
      const valid = panPattern.test(panInput.value);
      panInput.classList.toggle('success', valid);
      panInput.classList.toggle('error', !valid && panInput.value.length === 10);
      if (panTick) toggleClass(panTick, 'visible', valid);
    });
  }

  // Vehicle registration number
  const vrn = document.getElementById('vehicle-reg');
  const vrnTick = document.getElementById('vrn-tick');
  const vrnPattern = /^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$/;
  if (vrn) {
    vrn.addEventListener('input', () => {
      vrn.value = vrn.value.toUpperCase().replace(/[^A-Z0-9]/g, '').substring(0, 10);
      const valid = vrnPattern.test(vrn.value);
      vrn.classList.toggle('success', valid);
      vrn.classList.toggle('error', !valid && vrn.value.length >= 8);
      if (vrnTick) toggleClass(vrnTick, 'visible', valid);
    });
  }

  // Vehicle type — reveal permit field
  const vehicleTypeSelect = document.getElementById('vehicle-type');
  const permitGroup = document.getElementById('permit-group');
  if (vehicleTypeSelect && permitGroup) {
    vehicleTypeSelect.addEventListener('change', () => {
      const val = vehicleTypeSelect.value;
      const showPermit = val === 'commercial' || val === 'heavy';
      toggleClass(permitGroup, 'hidden', !showPermit);
    });
  }

  // Password strength
  initPasswordStrength('create-password', 'strength-bar-signup', 'strength-label-signup', 'pw-checklist-signup');

  // Confirm password mismatch
  const confirmPw = document.getElementById('confirm-password');
  const confirmErr = document.getElementById('confirm-pw-error');
  const createPw = document.getElementById('create-password');
  if (confirmPw && confirmErr && createPw) {
    confirmPw.addEventListener('blur', () => {
      const mismatch = confirmPw.value !== createPw.value;
      toggleClass(confirmErr, 'visible', mismatch && confirmPw.value.length > 0);
      toggleClass(confirmPw, 'error', mismatch && confirmPw.value.length > 0);
    });
    confirmPw.addEventListener('input', () => {
      if (confirmErr.classList.contains('visible')) {
        const mismatch = confirmPw.value !== createPw.value;
        toggleClass(confirmErr, 'visible', mismatch);
        toggleClass(confirmPw, 'error', mismatch);
      }
    });
  }

  // Terms modal
  initModal('terms-link', 'terms-modal', 'terms-modal-close');
  initModal('privacy-link', 'privacy-modal', 'privacy-modal-close');

  // Create Account button — enable only when checkboxes checked + passwords match
  const cb1 = document.getElementById('cb-accuracy');
  const cb2 = document.getElementById('cb-terms');
  const createBtn = document.getElementById('create-account-btn');

  function updateCreateBtn() {
    if (!createBtn || !cb1 || !cb2 || !createPw || !confirmPw) return;
    const checked = cb1.checked && cb2.checked;
    const pwMatch = createPw.value.length >= 8 && createPw.value === confirmPw.value;
    createBtn.disabled = !(checked && pwMatch);
  }

  if (cb1) cb1.addEventListener('change', updateCreateBtn);
  if (cb2) cb2.addEventListener('change', updateCreateBtn);
  if (createPw) createPw.addEventListener('input', updateCreateBtn);
  if (confirmPw) confirmPw.addEventListener('input', updateCreateBtn);
  updateCreateBtn();
}

/* =========================================================
   PASSWORD STRENGTH METER
   ========================================================= */

/**
 * @param {string} inputId
 * @param {string} barId - id of the .strength-bar container
 * @param {string} labelId - id of the .strength-label span
 * @param {string} checklistId - id of the .pw-checklist ul
 */
function initPasswordStrength(inputId, barId, labelId, checklistId) {
  const input = document.getElementById(inputId);
  const bar = document.getElementById(barId);
  const label = document.getElementById(labelId);
  const checklist = document.getElementById(checklistId);
  if (!input || !bar) return;

  const levels = ['', 'strength-tooshort', 'strength-weak', 'strength-fair', 'strength-good', 'strength-strong'];
  const levelNames = ['', 'Too short', 'Weak', 'Fair', 'Good', 'Strong'];

  function getLevel(val) {
    if (val.length === 0) return 0;
    if (val.length < 8) return 1;
    let score = 0;
    if (/[A-Z]/.test(val)) score++;
    if (/[0-9]/.test(val)) score++;
    if (/[!@#$%^&*]/.test(val)) score++;
    if (val.length >= 8 && score === 0) return 2;
    if (val.length >= 8 && score === 1) return 3;
    if (val.length >= 8 && score === 2) return 4;
    if (val.length >= 8 && score === 3) return 5;
    return 2;
  }

  function updateChecklist(val) {
    if (!checklist) return;
    const items = checklist.querySelectorAll('.pw-check-item');
    const conditions = [
      val.length >= 8,
      /[A-Z]/.test(val),
      /[0-9]/.test(val),
      /[!@#$%^&*]/.test(val),
    ];
    items.forEach((item, i) => {
      toggleClass(item, 'met', conditions[i] === true);
    });
  }

  input.addEventListener('input', () => {
    const val = input.value;
    const level = getLevel(val);

    // Remove all level classes
    levels.forEach(cls => { if (cls) bar.classList.remove(cls); });

    if (level > 0) {
      bar.classList.add(levels[level]);
    }

    if (label) {
      label.textContent = levelNames[level];
    }

    updateChecklist(val);
  });
}

/* =========================================================
   OTP VERIFY PAGE
   ========================================================= */

function initOtpVerify() {
  const inputs = document.querySelectorAll('.otp-input');
  const verifyBtn = document.getElementById('verify-otp-btn');
  const otpError = document.getElementById('otp-error');
  const form = document.getElementById('otp-form');

  // Auto-focus management
  inputs.forEach((input, index) => {
    input.addEventListener('input', (e) => {
      // Only allow digits
      input.value = input.value.replace(/\D/g, '').substring(0, 1);

      if (input.value && index < inputs.length - 1) {
        inputs[index + 1].focus();
      }

      // Auto-submit when all filled
      const allFilled = Array.from(inputs).every(i => i.value.length === 1);
      if (allFilled && verifyBtn) {
        verifyBtn.disabled = false;
        // Simulate auto-submit after short delay
        setTimeout(() => {
          handleOtpVerify();
        }, 200);
      }
    });

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Backspace') {
        if (!input.value && index > 0) {
          inputs[index - 1].focus();
          inputs[index - 1].value = '';
        }
      }
      if (e.key === 'ArrowLeft' && index > 0) inputs[index - 1].focus();
      if (e.key === 'ArrowRight' && index < inputs.length - 1) inputs[index + 1].focus();
    });

    // Allow paste of 6-digit OTP
    input.addEventListener('paste', (e) => {
      e.preventDefault();
      const pasted = (e.clipboardData || window.clipboardData).getData('text').replace(/\D/g, '');
      pasted.split('').slice(0, inputs.length).forEach((ch, i) => {
        if (inputs[i]) inputs[i].value = ch;
      });
      const last = Math.min(pasted.length, inputs.length) - 1;
      if (inputs[last]) inputs[last].focus();
    });
  });

  // Focus first input on load
  if (inputs[0]) inputs[0].focus();

  let otpAttempts = 0;

  function handleOtpVerify() {
    const otp = Array.from(inputs).map(i => i.value).join('');
    if (otp.length === 6) {
      // Simulate: any 6-digit OTP is "correct" for demo
      // On success redirect to signup
      window.location.href = '/signup';
    } else {
      otpAttempts += 1;
      inputs.forEach(i => i.classList.add('error'));
      if (otpError) {
        const remaining = Math.max(0, 3 - otpAttempts);
        otpError.textContent = `Incorrect OTP. ${remaining} attempt${remaining !== 1 ? 's' : ''} remaining.`;
        otpError.classList.add('visible');
      }
    }
  }

  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      handleOtpVerify();
    });
  }

  // Resend OTP countdown
  const resendBtn = document.getElementById('resend-otp-btn');
  const resendCountdown = document.getElementById('resend-countdown');
  startResendCountdown(resendBtn, resendCountdown, 60);
}

/**
 * Generic resend countdown.
 * @param {Element} btn - the resend button
 * @param {Element} countdownEl - element showing countdown text
 * @param {number} seconds - countdown duration
 */
function startResendCountdown(btn, countdownEl, seconds) {
  if (!btn || !countdownEl) return;
  btn.disabled = true;
  let remaining = seconds;

  countdownEl.textContent = `Resend available in ${formatTime(remaining)}`;
  show(countdownEl);

  const interval = setInterval(() => {
    remaining -= 1;
    countdownEl.textContent = `Resend available in ${formatTime(remaining)}`;
    if (remaining <= 0) {
      clearInterval(interval);
      btn.disabled = false;
      hide(countdownEl);
    }
  }, 1000);
}

/* =========================================================
   FORGOT PASSWORD PAGE
   ========================================================= */

function initForgotPassword() {
  const stage1 = document.getElementById('fp-stage-1');
  const stage2 = document.getElementById('fp-stage-2');
  const emailInput = document.getElementById('fp-email');
  const sendBtn = document.getElementById('send-reset-btn');
  const maskedEmailEl = document.getElementById('masked-email');
  const resendBtn = document.getElementById('resend-link-btn');
  const resendCountdown = document.getElementById('fp-resend-countdown');

  function maskEmail(email) {
    if (!email || !email.includes('@')) return email;
    const [local, domain] = email.split('@');
    const visible = local.substring(0, 2);
    return `${visible}***@${domain}`;
  }

  if (sendBtn) {
    sendBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const email = emailInput ? emailInput.value.trim() : '';
      if (!email) {
        if (emailInput) {
          emailInput.classList.add('error');
          const errEl = document.getElementById('fp-email-error');
          if (errEl) errEl.classList.add('visible');
        }
        return;
      }
      if (maskedEmailEl) maskedEmailEl.textContent = maskEmail(email);
      if (stage1) stage1.classList.remove('active');
      if (stage2) stage2.classList.add('active');
      startResendCountdown(resendBtn, resendCountdown, 59);
    });
  }

  if (emailInput) {
    emailInput.addEventListener('input', () => {
      emailInput.classList.remove('error');
      const errEl = document.getElementById('fp-email-error');
      if (errEl) errEl.classList.remove('visible');
    });
  }
}

/* =========================================================
   RESET PASSWORD PAGE
   ========================================================= */

function initResetPassword() {
  initPasswordToggle('new-password', 'new-pw-toggle');
  initPasswordToggle('confirm-new-password', 'confirm-new-pw-toggle');
  initPasswordStrength('new-password', 'strength-bar-reset', 'strength-label-reset', 'pw-checklist-reset');

  // Confirm password mismatch
  const newPw = document.getElementById('new-password');
  const confirmPw = document.getElementById('confirm-new-password');
  const confirmErr = document.getElementById('reset-confirm-error');

  if (newPw && confirmPw && confirmErr) {
    confirmPw.addEventListener('blur', () => {
      const mismatch = confirmPw.value !== newPw.value;
      toggleClass(confirmErr, 'visible', mismatch && confirmPw.value.length > 0);
      toggleClass(confirmPw, 'error', mismatch && confirmPw.value.length > 0);
    });
    confirmPw.addEventListener('input', () => {
      if (confirmErr.classList.contains('visible')) {
        const mismatch = confirmPw.value !== newPw.value;
        toggleClass(confirmErr, 'visible', mismatch);
        toggleClass(confirmPw, 'error', mismatch);
      }
    });
  }

  // Password reuse check (hardcoded demo passwords)
  const OLD_PASSWORDS = ['Password1!', 'OldPass@2023', 'Fastag#123'];
  const reuseWarning = document.getElementById('pw-reuse-warning');

  if (newPw && reuseWarning) {
    newPw.addEventListener('blur', () => {
      const isReused = OLD_PASSWORDS.includes(newPw.value);
      toggleClass(reuseWarning, 'visible', isReused);
      toggleClass(newPw, 'error', isReused);
    });
    newPw.addEventListener('input', () => {
      if (reuseWarning.classList.contains('visible')) {
        const isReused = OLD_PASSWORDS.includes(newPw.value);
        toggleClass(reuseWarning, 'visible', isReused);
        toggleClass(newPw, 'error', isReused);
      }
    });
  }
}

/* =========================================================
   RESET SUCCESS PAGE
   ========================================================= */

function initResetSuccess() {
  const countdownEl = document.getElementById('redirect-countdown');
  let remaining = 5;

  if (countdownEl) countdownEl.textContent = `Redirecting in ${remaining}...`;

  const interval = setInterval(() => {
    remaining -= 1;
    if (countdownEl) countdownEl.textContent = `Redirecting in ${remaining}...`;
    if (remaining <= 0) {
      clearInterval(interval);
      window.location.href = '/login';
    }
  }, 1000);
}

/* =========================================================
   MPIN SETUP PAGE
   ========================================================= */

function initMpinSetup() {
  const mpinInputs = document.querySelectorAll('.mpin-create .mpin-input');
  const mpinConfirmInputs = document.querySelectorAll('.mpin-confirm .mpin-input');
  const mpinError = document.getElementById('mpin-error');
  const setMpinBtn = document.getElementById('set-mpin-btn');
  const form = document.getElementById('mpin-form');

  function wireInputs(inputs) {
    inputs.forEach((input, index) => {
      input.addEventListener('input', () => {
        input.value = input.value.replace(/\D/g, '').substring(0, 1);
        if (input.value && index < inputs.length - 1) {
          inputs[index + 1].focus();
        }
      });
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Backspace' && !input.value && index > 0) {
          inputs[index - 1].focus();
          inputs[index - 1].value = '';
        }
      });
    });
  }

  wireInputs(mpinInputs);
  wireInputs(mpinConfirmInputs);

  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const mpin = Array.from(mpinInputs).map(i => i.value).join('');
      const confirm = Array.from(mpinConfirmInputs).map(i => i.value).join('');

      if (mpin.length < 4) {
        mpinError.textContent = 'Please enter a 4–6 digit MPIN.';
        mpinError.classList.add('visible');
        return;
      }

      if (mpin !== confirm) {
        mpinError.textContent = 'MPINs do not match';
        mpinError.classList.add('visible');
        mpinConfirmInputs.forEach(i => i.classList.add('error'));
        return;
      }

      mpinError.classList.remove('visible');
      // Success — redirect to login
      window.location.href = '/login';
    });
  }
}

/* =========================================================
   MODAL HELPER
   ========================================================= */

/**
 * Wire a link to open a modal, and wire the close button.
 * @param {string} triggerLinkId
 * @param {string} modalId
 * @param {string} closeId
 */
function initModal(triggerLinkId, modalId, closeId) {
  const trigger = document.getElementById(triggerLinkId);
  const modal = document.getElementById(modalId);
  const closeBtn = document.getElementById(closeId);

  if (!trigger || !modal) return;

  function openModal(e) {
    e.preventDefault();
    modal.classList.add('open');
    document.body.style.overflow = 'hidden';
    // Focus close button for accessibility
    if (closeBtn) setTimeout(() => closeBtn.focus(), 50);
  }

  function closeModal() {
    modal.classList.remove('open');
    document.body.style.overflow = '';
    trigger.focus();
  }

  trigger.addEventListener('click', openModal);
  if (closeBtn) closeBtn.addEventListener('click', closeModal);

  // Close on overlay click
  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });

  // Close on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('open')) closeModal();
  });
}
