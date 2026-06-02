Login Screen
Heading: Welcome Back
Subheading: Sign in to your FASTag account
Field 1 label: Mobile Number
Field 1 placeholder: Enter your registered mobile number
Field 2 label: Password
Field 2 placeholder: Enter your password
Toggle link: Show / Hide
Forgot password link: Forgot password?
Primary button: Sign In
Divider: or
Alt buttons: Continue with Google · Continue with Net Banking
Switch prompt: New to FASTag? Create an account

Sign Up Page — Updated Content
Heading: FASTag Account Registration
Subheading: Complete the form below to apply for your FASTag
Progress steps: Personal Details → Address & Vehicle Details → Confirmation

Step 1 — Personal Details
Section heading: Personal Details
Section note: Enter your details exactly as per PAN records
Field 1 label: PAN Number (mandatory)
Field 1 placeholder: Enter 10-character PAN
Helper text: Kindly enter name and date of birth as per PAN records
Inline action button: Verify PAN
Field 2 label: Date of Birth (mandatory)
Field 2 placeholder: DD / MM / YYYY
Inline error: Applicant must be 18 years or older to apply
Field 3 label: First Name (mandatory)
Field 3 placeholder: As per PAN card
Field 4 label: Last Name (mandatory)
Field 4 placeholder: As per PAN card
Field 5 label: Mother's Maiden Name (mandatory)
Field 5 placeholder: Enter mother's maiden name
Field 6 label: Gender (mandatory)
Dropdown options: Select · Male · Female · Transgender
Field 7 label: Aadhaar Number (mandatory)
Field 7 placeholder: Enter 12-digit Aadhaar number
Helper text: First 8 digits will be masked for security
Field 8 label: Mobile Number (mandatory)
Field 8 placeholder: Enter 10-digit mobile number
Helper text: OTP will be sent to this number for verification
Field 9 label: Email ID (mandatory)
Field 9 placeholder: Enter your email address
Field 10 label: Select ID Proof (mandatory)
Dropdown options: Select · Driving Licence · Voter ID Card · Passport (first & last page)
Field 11 label: ID Proof Number (mandatory)
Field 11 placeholder: Enter ID proof number
Upload label: Upload ID Proof
Upload helper: Ensure filename has no special characters. Accepted formats: JPG, PNG, PDF. Max size: 2MB
Upload success message: Your file has been uploaded successfully.
Note at bottom: *(mandatory) fields are required. Application applicable for Car, Jeep, and Light Motor Vehicles only.
Button: Continue

Step 2 — Address & Vehicle Details
Section heading: Address Details
Field 1 label: Address Line 1 (mandatory)
Field 1 placeholder: House / Flat No., Building Name
Field 2 label: Address Line 2
Field 2 placeholder: Street, Area, Locality
Field 3 label: City (mandatory)
Field 3 placeholder: Enter city name
Field 4 label: State (mandatory)
Dropdown: Select State
Field 5 label: PIN Code (mandatory)
Field 5 placeholder: Enter 6-digit PIN code

Step 2 — Vehicle Details (Updated)
Section heading: Vehicle Details
Field 1 label: Do you have a permanent Registration Number?
Options (radio): Yes, I have my RC · No, I have a new vehicle (chassis number only)

If "Yes" is selected:
Field 2 label: Vehicle Registration Number (mandatory)
Field 2 placeholder: e.g. TN01AB1234
Helper text: Enter exactly as printed on your Registration Certificate (RC)

If "No" is selected:
Field 2 label: Chassis Number / VIN (mandatory)
Field 2 placeholder: Enter full chassis number
Helper text: Found on your RC book, invoice, or vehicle frame near the dashboard
Info banner: You are registering FASTag using a chassis number. As per NHAI guidelines, you must update this to your permanent Vehicle Registration Number within 90–180 days of FASTag issuance. Failure to do so may result in tag deactivation.
Warning note: Monthly and annual toll passes cannot be issued on FASTag registered with a chassis number. Update to a permanent vehicle number first to avail these benefits.

Common fields for both:
Field 3 label: Vehicle Type / Class (mandatory)
Dropdown options: Select · Car / Jeep / Light Motor Vehicle · Two Wheeler · Commercial Vehicle · Heavy Vehicle
Field 4 label: Vehicle Make (mandatory)
Field 4 placeholder: e.g. Maruti, Hyundai, Tata
Field 5 label: Vehicle Model (mandatory)
Field 5 placeholder: e.g. Swift, i20, Nexon
Field 6 label: Chassis Number — Last 5 Digits (mandatory)
Field 6 placeholder: e.g. AB123
Helper text: Required for identity verification against your RC
Upload label: Upload RC Copy (mandatory)
Upload helper: Upload front and back of your Registration Certificate. If RC is not yet issued, upload your vehicle purchase invoice. Accepted: JPG, PNG, PDF. Max size: 2MB

Update Reminder (shown post-registration on dashboard):
Banner heading: Action Required — Update Vehicle Number
Banner message: Your FASTag is currently linked to a chassis number. Please update your permanent Vehicle Registration Number within 90 days to avoid deactivation and to unlock monthly and annual toll pass benefits.
Banner button: Update Vehicle Number Now

Section heading: Account Security
Field 11 label: Create Password (mandatory)
Field 11 placeholder: Minimum 8 characters
Helper text: Must include uppercase, number, and special character
Section 4 — Account Security
Field 9 label: Create Password
Field 9 placeholder: Minimum 8 characters
Helper text: Use uppercase, numbers, and special characters(make it as a checklist)
Password strength labels: Too short · Weak · Fair · Good · Strong
Field 12 label: Confirm Password (mandatory)
Field 12 placeholder: Re-enter your password
Inline error: Passwords do not match
Add: MPIN setup — after creating the account, prompt users to set a 4–6 digit MPIN for quicker future logins.
Tune: The T&C and Privacy Policy links should open in a modal/bottom sheet, not a new tab — especially on mobile, leaving the sign-up form to read T&C in a new tab causes drop-off.


Checkbox 1: I confirm that the details provided are true and match my official documents.
Checkbox 2: I agree to the Terms & Conditions and Privacy Policy of the FASTag portal.
Button: Submit Application
Back button: ← Previous Step

Step 3 — Confirmation
Heading: Application Submitted Successfully
Subheading: Your FASTag registration request has been received.
Info block:

Application Reference Number: FT2024XXXXXXXX
Registered Mobile: +91 98XXXXX234
Registered Email: ra***@gmail.com**
Vehicle Number: TN01AB1234

Next steps message: Your KYC documents will be verified within 2–3 working days. You will receive an SMS and email confirmation once your FASTag is activated. Your physical FASTag sticker will be dispatched to your registered address within 7 working days.
Button: Go to Login
Secondary link: Download Acknowledgement

Switch prompt: Already have an account? Sign in

Forgot Password — Email Flow
Stage 1 — Enter Email
Heading: Forgot Password?
Subheading: Enter the email address linked to your FASTag account. We'll send you a reset link.
Field label: Registered Email Address
Field placeholder: Enter your email address
Helper text: Make sure you have access to this inbox
Primary button: Send Reset Link
Footer link: ← Back to Login

Stage 2 — Email Sent Confirmation
Heading: Check Your Inbox
Subheading: A password reset link has been sent to ra***@gmail.com**

OTP verification screen — triggered after phone number entry in sign-up. Needs: 6-digit input, resend with cooldown, wrong OTP error state.

Info message: The link will expire in 30 minutes. If you don't see it, check your spam folder.
Resend prompt: Didn't receive the email? Resend link
Cooldown text: Resend available in 00:59
Footer link: ← Back to Login

Stage 3 — Reset Password (from email link/SMS OTP)
Heading: Set New Password
Subheading: Choose a strong password for your account
Field 1 label: New Password
Field 1 placeholder: Minimum 8 characters
Password strength labels: Too short · Weak · Fair · Good · Strong
Field 2 label: Confirm New Password
Field 2 placeholder: Re-enter new password
Inline error: Passwords do not match
Primary button: Update Password

Add: Password reuse check — on Stage 3 (reset), block the user from reusing their last 2–3 passwords and show a clear error if they try.



Stage 4 — Success
Heading: Password Updated!
Subheading: Your password has been reset successfully. You can now sign in with your new password.
Primary button: Go to Login 
