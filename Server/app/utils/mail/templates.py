def registration_mail(name: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Registration Successful</title>
    </head>

    <body style="margin:0; padding:0; background-color:#f4f7fb; font-family:Arial, Helvetica, sans-serif;">

    <table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#f4f7fb">
        <tr>
        <td align="center" style="padding:40px 20px;">

            <!-- Main Container -->
            <table width="600" cellpadding="0" cellspacing="0" border="0"
            style="max-width:600px; background:#ffffff; border-radius:14px; overflow:hidden; box-shadow:0 4px 20px rgba(0,0,0,0.08);">

            <!-- Header -->
            <tr>
                <td align="center"
                style="background:linear-gradient(135deg, #111827, #1f2937); padding:40px 30px;">

                <img
                    src="YOUR_LOGO_URL"
                    alt="YOUR_APP_NAME"
                    width="70"
                    style="display:block; margin-bottom:18px;"
                />

                <h1 style="margin:0; color:#ffffff; font-size:28px; font-weight:700;">
                    YOUR_APP_NAME
                </h1>

                <p style="margin-top:10px; color:#cbd5e1; font-size:15px; line-height:24px;">
                    AI-Powered RAG Platform built with Modern LLM Intelligence
                </p>
                </td>
            </tr>

            <!-- Content -->
            <tr>
                <td style="padding:45px 40px; color:#111827;">

                <h2 style="margin:0 0 20px; font-size:26px; color:#111827;">
                    Welcome, {name} 👋
                </h2>

                <p style="font-size:16px; line-height:28px; color:#4b5563; margin:0 0 20px;">
                    Your registration was completed successfully.
                </p>

                <p style="font-size:16px; line-height:28px; color:#4b5563; margin:0 0 20px;">
                    You now have access to an advanced AI-powered RAG platform designed
                    to help you interact with Large Language Models intelligently,
                    retrieve contextual knowledge, and build smarter workflows.
                </p>

                <!-- Feature Box -->
                <table width="100%" cellpadding="0" cellspacing="0" border="0"
                    style="background:#f9fafb; border:1px solid #e5e7eb; border-radius:12px; margin:30px 0;">

                    <tr>
                    <td style="padding:25px;">

                        <h3 style="margin:0 0 15px; color:#111827; font-size:18px;">
                        What You Can Do
                        </h3>

                        <p style="margin:8px 0; color:#4b5563; font-size:15px;">
                        ✅ AI-Powered Retrieval & Knowledge Search
                        </p>

                        <p style="margin:8px 0; color:#4b5563; font-size:15px;">
                        ✅ Context-Aware LLM Responses
                        </p>

                        <p style="margin:8px 0; color:#4b5563; font-size:15px;">
                        ✅ Upload & Query Documents
                        </p>

                        <p style="margin:8px 0; color:#4b5563; font-size:15px;">
                        ✅ Build Intelligent AI Workflows
                        </p>

                    </td>
                    </tr>

                </table>

                <!-- CTA Button -->
                <table cellpadding="0" cellspacing="0" border="0" align="center" style="margin:35px auto;">
                    <tr>
                    <td align="center" bgcolor="#111827" style="border-radius:10px;">
                        <a href="https://yourapp.com/dashboard"
                        style="display:inline-block; padding:16px 32px; font-size:16px; color:#ffffff; text-decoration:none; font-weight:bold;">
                        Go To Dashboard
                        </a>
                    </td>
                    </tr>
                </table>

                <p style="font-size:15px; line-height:26px; color:#6b7280; margin-top:30px;">
                    If you have any questions, simply reply to this email.
                    We're excited to have you onboard.
                </p>

                <p style="font-size:16px; color:#111827; margin-top:30px; font-weight:bold;">
                    — The YOUR_APP_NAME Team
                </p>

                </td>
            </tr>

            <!-- Footer -->
            <tr>
                <td align="center"
                style="background:#f9fafb; padding:25px 30px; border-top:1px solid #e5e7eb;">

                <p style="margin:0; font-size:13px; color:#9ca3af; line-height:22px;">
                    © 2026 YOUR_APP_NAME. All rights reserved.
                </p>

                <p style="margin-top:8px; font-size:13px; color:#9ca3af;">
                    AI • RAG • LLM • Intelligent Knowledge Systems
                </p>

                </td>
            </tr>

            </table>

        </td>
        </tr>
    </table>

    </body>
    </html>
    """

def verification_otp(name: str, otp: str) -> str:
    return f"""
        <!DOCTYPE html>
        <html lang="en">

        <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>Verify Your Email</title>
        </head>

        <body style="margin:0; padding:0; background-color:#f4f7fb; font-family:Arial, Helvetica, sans-serif;">

        <table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#f4f7fb">
            <tr>
            <td align="center" style="padding:40px 20px;">

                <!-- Main Container -->
                <table width="600" cellpadding="0" cellspacing="0" border="0"
                style="max-width:600px; background:#ffffff; border-radius:14px; overflow:hidden; box-shadow:0 4px 20px rgba(0,0,0,0.08);">

                <!-- Header -->
                <tr>
                    <td align="center"
                    style="background:linear-gradient(135deg, #111827, #1f2937); padding:40px 30px;">

                    <img
                        src="https://res.cloudinary.com/ddiaarexp/image/upload/v1778473410/ChatGPT_Image_May_11_2026_09_49_15_AM_a8u8ti.png"
                        alt="UV's Rag"
                        width="75"
                        style="display:block; margin-bottom:18px;"
                    />

                    <h1 style="margin:0; color:#ffffff; font-size:28px; font-weight:700;">
                        UV's Rag
                    </h1>

                    <p style="margin-top:10px; color:#cbd5e1; font-size:15px; line-height:24px;">
                        AI-Powered RAG Platform built with Modern LLM Intelligence
                    </p>
                    </td>
                </tr>

                <!-- Content -->
                <tr>
                    <td style="padding:45px 40px; color:#111827;">

                    <h2 style="margin:0 0 20px; font-size:26px; color:#111827;">
                        Verify Your Email Address
                    </h2>

                    <p style="font-size:16px; line-height:28px; color:#4b5563; margin:0 0 20px;">
                        Hello <strong>{name}</strong>,
                    </p>

                    <p style="font-size:16px; line-height:28px; color:#4b5563; margin:0 0 20px;">
                        Thank you for signing up for <strong>UV's Rag</strong>.
                        Please use the verification code below to verify your email address.
                    </p>

                    <!-- OTP Box -->
                    <table width="100%" cellpadding="0" cellspacing="0" border="0"
                        style="margin:35px 0;">

                        <tr>
                        <td align="center">

                            <div style="
                            display:inline-block;
                            background:#111827;
                            color:#ffffff;
                            font-size:34px;
                            letter-spacing:10px;
                            font-weight:bold;
                            padding:18px 35px;
                            border-radius:14px;
                            ">
                            {otp}
                            </div>

                        </td>
                        </tr>

                    </table>

                    <p style="font-size:15px; line-height:26px; color:#6b7280; margin-top:10px;">
                        This OTP is valid for the next <strong>10 minutes</strong>.
                        Please do not share this code with anyone.
                    </p>

                    <!-- Security Box -->
                    <table width="100%" cellpadding="0" cellspacing="0" border="0"
                        style="background:#f9fafb; border:1px solid #e5e7eb; border-radius:12px; margin:30px 0;">

                        <tr>
                        <td style="padding:22px;">

                            <h3 style="margin:0 0 12px; color:#111827; font-size:18px;">
                            Security Notice
                            </h3>

                            <p style="margin:0; color:#4b5563; font-size:15px; line-height:26px;">
                            If you did not create an account with UV's Rag,
                            you can safely ignore this email.
                            </p>

                        </td>
                        </tr>

                    </table>

                    <p style="font-size:15px; line-height:26px; color:#6b7280; margin-top:30px;">
                        Need help? Simply reply to this email and our support team will assist you.
                    </p>

                    <p style="font-size:16px; color:#111827; margin-top:30px; font-weight:bold;">
                        — The UV's Rag Team
                    </p>

                    </td>
                </tr>

                <!-- Footer -->
                <tr>
                    <td align="center"
                    style="background:#f9fafb; padding:25px 30px; border-top:1px solid #e5e7eb;">

                    <p style="margin:0; font-size:13px; color:#9ca3af; line-height:22px;">
                        © 2026 UV's Rag. All rights reserved.
                    </p>

                    <p style="margin-top:8px; font-size:13px; color:#9ca3af;">
                        AI • RAG • LLM • Intelligent Knowledge Systems
                    </p>

                    </td>
                </tr>

                </table>

            </td>
            </tr>
        </table>

        </body>
        </html>
        """

def verified_mail(name: str) -> str:
    return f"""
        <!DOCTYPE html>
        <html lang="en">

        <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>Account Verified</title>
        </head>

        <body style="margin:0; padding:0; background-color:#f4f7fb; font-family:Arial, Helvetica, sans-serif;">

        <table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#f4f7fb">
            <tr>
            <td align="center" style="padding:40px 20px;">

                <!-- Main Container -->
                <table width="600" cellpadding="0" cellspacing="0" border="0"
                style="max-width:600px; background:#ffffff; border-radius:14px; overflow:hidden; box-shadow:0 4px 20px rgba(0,0,0,0.08);">

                <!-- Header -->
                <tr>
                    <td align="center"
                    style="background:linear-gradient(135deg, #111827, #1f2937); padding:40px 30px;">

                    <img
                        src="https://res.cloudinary.com/ddiaarexp/image/upload/v1778473410/ChatGPT_Image_May_11_2026_09_49_15_AM_a8u8ti.png"
                        alt="UV's Rag"
                        width="75"
                        style="display:block; margin-bottom:18px;"
                    />

                    <h1 style="margin:0; color:#ffffff; font-size:28px; font-weight:700;">
                        UV's Rag
                    </h1>

                    <p style="margin-top:10px; color:#cbd5e1; font-size:15px; line-height:24px;">
                        AI-Powered RAG Platform built with Modern LLM Intelligence
                    </p>
                    </td>
                </tr>

                <!-- Content -->
                <tr>
                    <td style="padding:45px 40px; color:#111827;">

                    <div style="text-align:center; margin-bottom:30px;">
                        <div style="
                        width:90px;
                        height:90px;
                        background:#dcfce7;
                        border-radius:50%;
                        display:inline-flex;
                        align-items:center;
                        justify-content:center;
                        font-size:42px;
                        ">
                        ✅
                        </div>
                    </div>

                    <h2 style="margin:0 0 20px; font-size:28px; color:#111827; text-align:center;">
                        Account Verification Completed
                    </h2>

                    <p style="font-size:16px; line-height:28px; color:#4b5563; margin:0 0 20px; text-align:center;">
                        Hello <strong>{name}</strong>,
                    </p>

                    <p style="font-size:16px; line-height:28px; color:#4b5563; margin:0 0 25px; text-align:center;">
                        Your email address has been successfully verified.
                        Your UV's Rag account is now fully activated and ready to use.
                    </p>

                    <!-- Success Box -->
                    <table width="100%" cellpadding="0" cellspacing="0" border="0"
                        style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:12px; margin:30px 0;">

                        <tr>
                        <td style="padding:24px;">

                            <h3 style="margin:0 0 15px; color:#166534; font-size:18px;">
                            Your Account is Ready
                            </h3>

                            <p style="margin:8px 0; color:#166534; font-size:15px;">
                            ✅ Email successfully verified
                            </p>

                            <p style="margin:8px 0; color:#166534; font-size:15px;">
                            ✅ Access to AI-powered RAG tools
                            </p>

                            <p style="margin:8px 0; color:#166534; font-size:15px;">
                            ✅ Start querying documents & knowledge bases
                            </p>

                            <p style="margin:8px 0; color:#166534; font-size:15px;">
                            ✅ Build intelligent LLM workflows
                            </p>

                        </td>
                        </tr>

                    </table>

                    <!-- CTA Button -->
                    <table cellpadding="0" cellspacing="0" border="0" align="center" style="margin:35px auto;">
                        <tr>
                        <td align="center" bgcolor="#111827" style="border-radius:10px;">
                            <a href="https://yourapp.com/dashboard"
                            style="display:inline-block; padding:16px 32px; font-size:16px; color:#ffffff; text-decoration:none; font-weight:bold;">
                            Launch Dashboard
                            </a>
                        </td>
                        </tr>
                    </table>

                    <p style="font-size:15px; line-height:26px; color:#6b7280; margin-top:30px; text-align:center;">
                        Thank you for joining UV's Rag.
                        We're excited to help you build with AI and LLM-powered intelligence.
                    </p>

                    <p style="font-size:16px; color:#111827; margin-top:30px; font-weight:bold; text-align:center;">
                        — The UV's Rag Team
                    </p>

                    </td>
                </tr>

                <!-- Footer -->
                <tr>
                    <td align="center"
                    style="background:#f9fafb; padding:25px 30px; border-top:1px solid #e5e7eb;">

                    <p style="margin:0; font-size:13px; color:#9ca3af; line-height:22px;">
                        © 2026 UV's Rag. All rights reserved.
                    </p>

                    <p style="margin-top:8px; font-size:13px; color:#9ca3af;">
                        AI • RAG • LLM • Intelligent Knowledge Systems
                    </p>

                    </td>
                </tr>

                </table>

            </td>
            </tr>
        </table>

        </body>
        </html>
    """

def forget_passowrd_otp(name: str, otp: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="en">

    <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Reset Your Password</title>
    </head>

    <body style="margin:0; padding:0; background-color:#f4f7fb; font-family:Arial, Helvetica, sans-serif;">

    <table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#f4f7fb">
        <tr>
        <td align="center" style="padding:40px 20px;">

            <!-- Main Container -->
            <table width="600" cellpadding="0" cellspacing="0" border="0"
            style="max-width:600px; background:#ffffff; border-radius:14px; overflow:hidden; box-shadow:0 4px 20px rgba(0,0,0,0.08);">

            <!-- Header -->
            <tr>
                <td align="center"
                style="background:linear-gradient(135deg, #111827, #1f2937); padding:40px 30px;">

                <img
                    src="https://res.cloudinary.com/ddiaarexp/image/upload/v1778473410/ChatGPT_Image_May_11_2026_09_49_15_AM_a8u8ti.png"
                    alt="UV's Rag"
                    width="75"
                    style="display:block; margin-bottom:18px;"
                />

                <h1 style="margin:0; color:#ffffff; font-size:28px; font-weight:700;">
                    UV's Rag
                </h1>

                <p style="margin-top:10px; color:#cbd5e1; font-size:15px; line-height:24px;">
                    AI-Powered RAG Platform built with Modern LLM Intelligence
                </p>
                </td>
            </tr>

            <!-- Content -->
            <tr>
                <td style="padding:45px 40px; color:#111827;">

                <div style="text-align:center; margin-bottom:30px;">
                    <div style="
                    width:90px;
                    height:90px;
                    background:#fef3c7;
                    border-radius:50%;
                    display:inline-flex;
                    align-items:center;
                    justify-content:center;
                    font-size:42px;
                    ">
                    🔐
                    </div>
                </div>

                <h2 style="margin:0 0 20px; font-size:28px; color:#111827; text-align:center;">
                    Reset Your Password
                </h2>

                <p style="font-size:16px; line-height:28px; color:#4b5563; margin:0 0 20px; text-align:center;">
                    Hello <strong>{name}</strong>,
                </p>

                <p style="font-size:16px; line-height:28px; color:#4b5563; margin:0 0 25px; text-align:center;">
                    We received a request to reset your UV's Rag account password.
                    Use the OTP below to continue resetting your password.
                </p>

                <!-- OTP Box -->
                <table width="100%" cellpadding="0" cellspacing="0" border="0"
                    style="margin:35px 0;">

                    <tr>
                    <td align="center">

                        <div style="
                        display:inline-block;
                        background:#111827;
                        color:#ffffff;
                        font-size:34px;
                        letter-spacing:10px;
                        font-weight:bold;
                        padding:18px 35px;
                        border-radius:14px;
                        ">
                        {otp}
                        </div>

                    </td>
                    </tr>

                </table>

                <p style="font-size:15px; line-height:26px; color:#6b7280; margin-top:10px; text-align:center;">
                    This OTP is valid for the next <strong>10 minutes</strong>.
                </p>

                <!-- Security Notice -->
                <table width="100%" cellpadding="0" cellspacing="0" border="0"
                    style="background:#f9fafb; border:1px solid #e5e7eb; border-radius:12px; margin:30px 0;">

                    <tr>
                    <td style="padding:24px;">

                        <h3 style="margin:0 0 15px; color:#111827; font-size:18px;">
                        Security Notice
                        </h3>

                        <p style="margin:0 0 12px; color:#4b5563; font-size:15px; line-height:26px;">
                        Never share your OTP with anyone.
                        UV's Rag will never ask for your verification code.
                        </p>

                        <p style="margin:0; color:#4b5563; font-size:15px; line-height:26px;">
                        If you did not request a password reset,
                        you can safely ignore this email and your account will remain secure.
                        </p>

                    </td>
                    </tr>

                </table>

                <p style="font-size:15px; line-height:26px; color:#6b7280; margin-top:30px; text-align:center;">
                    Need help? Reply to this email and our support team will assist you.
                </p>

                <p style="font-size:16px; color:#111827; margin-top:30px; font-weight:bold; text-align:center;">
                    — The UV's Rag Team
                </p>

                </td>
            </tr>

            <!-- Footer -->
            <tr>
                <td align="center"
                style="background:#f9fafb; padding:25px 30px; border-top:1px solid #e5e7eb;">

                <p style="margin:0; font-size:13px; color:#9ca3af; line-height:22px;">
                    © 2026 UV's Rag. All rights reserved.
                </p>

                <p style="margin-top:8px; font-size:13px; color:#9ca3af;">
                    AI • RAG • LLM • Intelligent Knowledge Systems
                </p>

                </td>
            </tr>

            </table>

        </td>
        </tr>
    </table>

    </body>
    </html>
    """

def password_reset_template(name: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="en">

    <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Password Reset Successful</title>
    </head>

    <body style="margin:0; padding:0; background-color:#f4f7fb; font-family:Arial, Helvetica, sans-serif;">

    <table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#f4f7fb">
        <tr>
        <td align="center" style="padding:40px 20px;">

            <!-- Main Container -->
            <table width="600" cellpadding="0" cellspacing="0" border="0"
            style="max-width:600px; background:#ffffff; border-radius:14px; overflow:hidden; box-shadow:0 4px 20px rgba(0,0,0,0.08);">

            <!-- Header -->
            <tr>
                <td align="center"
                style="background:linear-gradient(135deg, #111827, #1f2937); padding:40px 30px;">

                <img
                    src="https://res.cloudinary.com/ddiaarexp/image/upload/v1778473410/ChatGPT_Image_May_11_2026_09_49_15_AM_a8u8ti.png"
                    alt="UV's Rag"
                    width="75"
                    style="display:block; margin-bottom:18px;"
                />

                <h1 style="margin:0; color:#ffffff; font-size:28px; font-weight:700;">
                    UV's Rag
                </h1>

                <p style="margin-top:10px; color:#cbd5e1; font-size:15px; line-height:24px;">
                    AI-Powered RAG Platform built with Modern LLM Intelligence
                </p>
                </td>
            </tr>

            <!-- Content -->
            <tr>
                <td style="padding:45px 40px; color:#111827;">

                <div style="text-align:center; margin-bottom:30px;">
                    <div style="
                    width:90px;
                    height:90px;
                    background:#dcfce7;
                    border-radius:50%;
                    display:inline-flex;
                    align-items:center;
                    justify-content:center;
                    font-size:42px;
                    ">
                    🔑
                    </div>
                </div>

                <h2 style="margin:0 0 20px; font-size:28px; color:#111827; text-align:center;">
                    Password Reset Successful
                </h2>

                <p style="font-size:16px; line-height:28px; color:#4b5563; margin:0 0 20px; text-align:center;">
                    Hello <strong>{name}</strong>,
                </p>

                <p style="font-size:16px; line-height:28px; color:#4b5563; margin:0 0 25px; text-align:center;">
                    Your UV's Rag account password has been successfully updated.
                    You can now securely log in using your new password.
                </p>

                <!-- Success Info Box -->
                <table width="100%" cellpadding="0" cellspacing="0" border="0"
                    style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:12px; margin:30px 0;">

                    <tr>
                    <td style="padding:24px;">

                        <h3 style="margin:0 0 15px; color:#166534; font-size:18px;">
                        Security Confirmation
                        </h3>

                        <p style="margin:8px 0; color:#166534; font-size:15px;">
                        ✅ Your password was successfully changed
                        </p>

                        <p style="margin:8px 0; color:#166534; font-size:15px;">
                        ✅ Your account remains secure
                        </p>

                        <p style="margin:8px 0; color:#166534; font-size:15px;">
                        ✅ You can now log in with your new credentials
                        </p>

                    </td>
                    </tr>

                </table>

                <!-- CTA Button -->
                <table cellpadding="0" cellspacing="0" border="0" align="center" style="margin:35px auto;">
                    <tr>
                    <td align="center" bgcolor="#111827" style="border-radius:10px;">
                        <a href="https://yourapp.com/login"
                        style="display:inline-block; padding:16px 32px; font-size:16px; color:#ffffff; text-decoration:none; font-weight:bold;">
                        Login to Your Account
                        </a>
                    </td>
                    </tr>
                </table>

                <!-- Security Warning -->
                <table width="100%" cellpadding="0" cellspacing="0" border="0"
                    style="background:#fef2f2; border:1px solid #fecaca; border-radius:12px; margin:30px 0;">

                    <tr>
                    <td style="padding:22px;">

                        <h3 style="margin:0 0 12px; color:#991b1b; font-size:18px;">
                        Didn't Reset Your Password?
                        </h3>

                        <p style="margin:0; color:#991b1b; font-size:15px; line-height:26px;">
                        If you did not perform this action,
                        please secure your account immediately and contact support.
                        </p>

                    </td>
                    </tr>

                </table>

                <p style="font-size:15px; line-height:26px; color:#6b7280; margin-top:30px; text-align:center;">
                    Thank you for keeping your account secure with UV's Rag.
                </p>

                <p style="font-size:16px; color:#111827; margin-top:30px; font-weight:bold; text-align:center;">
                    — The UV's Rag Team
                </p>

                </td>
            </tr>

            <!-- Footer -->
            <tr>
                <td align="center"
                style="background:#f9fafb; padding:25px 30px; border-top:1px solid #e5e7eb;">

                <p style="margin:0; font-size:13px; color:#9ca3af; line-height:22px;">
                    © 2026 UV's Rag. All rights reserved.
                </p>

                <p style="margin-top:8px; font-size:13px; color:#9ca3af;">
                    AI • RAG • LLM • Intelligent Knowledge Systems
                </p>

                </td>
            </tr>

            </table>

        </td>
        </tr>
    </table>

    </body>
    </html>
    """
