%%%
title = "FAPI 2.0 Implementation Advice"
abbrev = "fapi-2-implementation-advice"
ipr = "none"
workgroup = "fapi"
keyword = ["security", "openid", "fapi"]

[seriesInfo]
name = "Internet-Draft"
value = "fapi-2_0-implementation_advice-01"
status = "standard"

[[author]]
initials="D."
surname="Tonge"
fullname="Dave Tonge"
organization="Moneyhub Financial Technology"
    [author.address]
    email = "dave@tonge.org"

%%%

.# Abstract

Financial-grade API (FAPI) 2.0 Implementation Advice is a document to provide practical
guidance on the implementation and usage of the FAPI 2.0 family of standards.

.# Foreword

The OpenID Foundation (OIDF) promotes, protects and nurtures the OpenID community and technologies. As a non-profit international standardizing body, it is comprised by over 160 participating entities (workgroup participant). The work of preparing implementer drafts and final international standards is carried out through OIDF workgroups in accordance with the OpenID Process. Participants interested in a subject for which a workgroup has been established have the right to be represented in that workgroup. International organizations, governmental and non-governmental, in liaison with OIDF, also take part in the work. OIDF collaborates closely with other standardizing bodies in the related fields.

Final drafts adopted by the Workgroup through consensus are circulated publicly for the public review for 60 days and for the OIDF members for voting. Publication as an OIDF Standard requires approval by at least 50% of the members casting a vote. There is a possibility that some of the elements of this document may be subject to patent rights. OIDF shall not be held responsible for identifying any or all such patent rights.

.# Introduction

The Financial-grade API (FAPI) 2.0 family of standards provides security profiles and specifications
to enable implementers to deploy highly secure, interoperable APIs. While we have attempted 
to minimize the optionality in FAPI 2.0, there are still many decisions that need to be made by
implementers. This document aims to provide advice for implementers based on the experience
of members of the OpenID Foundation's FAPI Working Group.

.# Warning

This document is not an OIDF International Standard. It is distributed for
review and comment. It is subject to change without notice and may not be
referred to as an International Standard.

Recipients of this draft are invited to submit, with their comments,
notification of any relevant patent rights of which they are aware and to
provide supporting documentation.

.# Notational Conventions

The keywords "shall", "shall not", "should", "should not", "may", and "can" in
this document are to be interpreted as described in ISO Directive Part 2
[@ISODIR2]. These keywords are not used as dictionary terms such that any
occurrence of them shall be interpreted as keywords and are not to be
interpreted with their natural language meanings.

{mainmatter}

# Implementation Advice

## FAPI 2.0 Framework

The FAPI 2.0 Framework is comprised of several documents. At the time of writing, they are:

* FAPI 2.0 Attacker Model [@attackermodel];
* FAPI 2.0 Security Profile [@FAPI2_Security_Profile];
* FAPI 2.0 Message Signing [@FAPIMessageSigning] - for non repudiation of messages;
* FAPI Client Initiated Backchannel Authentication - for decoupled or cross device flows;
* Grant Management for OAuth 2.0 - for ecosystems that require interoperable grant management;
* OAuth 2.0 Rich Authorization Requests [@RFC9396] - for conveying complex authorizations.

The foundation of the framework is the attacker model and security profile. All the other 
specifications build on the security profile.

## HTTP Headers

Implementers may find the following http-headers useful:

### x-fapi-interaction-id

This header can be used to enable Authorization Servers, Resource Servers and Clients to
better track and debug any issues between them. If an ecosystem adopts `x-fapi-interaction-id` then 
the following clauses apply:


1. clients shall send the `x-fapi-interaction-id` request header, the value shall be a 
UUID [@RFC9562],  e.g., `x-fapi-interaction-id: c770aef3-6784-41f7-8e0e-ff5f97bddb3a`;
1. the AS or RS shall set the response header `x-fapi-interaction-id` to the value received from the corresponding FAPI client request header if that value is a UUID [@RFC9562], or otherwise to a new UUID [@RFC9562] value to track the interaction, e.g., `x-fapi-interaction-id: c770aef3-6784-41f7-8e0e-ff5f97bddb3a`;
1. participants (whether Client, AS or RS) shall log the value of `x-fapi-interaction-id` in the log entry.

NOTE: Clients may reuse the same `x-fapi-interaction-id` value across related requests within
a single authorization code flow, including PAR requests, token requests, and immediate 
API calls. This can help with tracing and troubleshooting related transactions. Due to the 
nature of browser redirects, the authorization request itself typically cannot include HTTP 
headers, so the `x-fapi-interaction-id` will not be present in those requests. Specific 
guidance on when to reuse vs. generate new interaction IDs may be defined by individual 
ecosystems.


### x-fapi-end-user-present

Many ecosystems have different non-functional requirements depending on whether an end-user
is present or not.  The `x-fapi-end-user-present` header indicates whether the request is 
being made in the context of an interactive end-user session or as part of a 
background/automated process. If an ecosystem adopts this header, the following clauses apply:

1. Clients shall send the `x-fapi-end-user-present` header with a value of `true` when 
the request is made with an end-user actively present in the session, and `false` when the 
request is part of a background process, batch operation, or automated task without active 
user participation.

2. If the header is not present, servers should assume a default value of `false` 
(i.e., no end-user is present).

3. The header value shall be a boolean: either `true` or `false`, 
e.g., `x-fapi-end-user-present: true`.

#### Purpose and Benefits

The primary benefit of the `x-fapi-end-user-present` header is to support 
ecosystem-specific requirements for different traffic patterns:

1. Many ecosystems implement different rate limits for end-user-present vs. background 
operations. User-present operations may have higher per-second limits but lower daily 
limits, while background operations might have the opposite pattern.

2. During high load situations, servers may prioritize user-present requests to 
maintain interactive performance while delaying background operations.

#### Implementation Considerations

1. This header is not a security mechanism. Authorization Servers must trust that 
Clients are filling in this header correctly and cannot independently verify the 
presence of an end user.

2. This header replaces problematic approaches from previous specifications, such as:
   - `x-fapi-customer-ip-address`: Potentially exposed PII and created privacy concerns
   - `x-fapi-auth-date`: Frequently implemented incorrectly and requires date parsing
   - Client headers pass-through: Inconsistently used and may expose PII

3. Since Clients can set this value arbitrarily, ecosystem governance and monitoring are 
necessary to detect patterns of misuse, such as clients marking all API calls as 
user-present regardless of context.

NOTE: This header is only useful in ecosystems where recourse exists against clients that falsify its value.

## DPoP vs MTLS

Sender constraining access tokens is an important security measure that provides significant protections against token theft and misuse. FAPI 2.0 allows implementers to use either DPoP or MTLS to achieve this goal. Both approaches meet the security requirements, but each has different characteristics that may make one more suitable than the other depending on your ecosystem. This section outlines considerations to guide your choice.

### DPoP Considerations

1. DPoP operates at the application layer rather than the transport layer;
2. DPoP only sender constrains part of the request (the HTTP method and URL), unlike MTLS which protects the entire request;
3. DPoP requires cryptographic operations for each request, which may have performance implications;
4. DPoP introduces protocol complexity, including HTTP request URL normalization and optionally server-provided nonces;
5. DPoP library support is less mature than MTLS, and there is limited ecosystem deployment experience;
6. DPoP is the only viable option for browser-based clients (MTLS only works practically for server-to-server communication).

### MTLS Considerations

1. MTLS performs both client authentication and sender constraining simultaneously, simplifying implementation for clients;
2. MTLS sender constrains the entire request, not just specific elements;
3. MTLS amortizes the cost of asymmetric cryptographic operations by performing them during the TLS handshake and reusing the connection;
4. Self-signed certificates can be used for sender constraining; the binding to the access token is established at the token endpoint without needing to distribute certificates via JWKS;
5. MTLS presents integration challenges at the transport layer, especially when operating at scale;
6. MTLS implementations may encounter interoperability issues with certificate handling, including:
   * Certificate aliases
   * IP/SAN negotiation
   * DN matching for PKI;
7. [RFC9440] provides additional guidance for MTLS implementations.

### Selection Guidance

Both DPoP and MTLS are valid choices for sender constraining, and each has trade-offs.

MTLS may be more suitable when:

* Operating in closed ecosystems with existing PKI infrastructure;
* Simplicity for client-side implementation is a priority;
* Full request protection is desired;
* Mature library support is required.

DPoP may be more suitable when:

* Browser-based clients need to be supported (MTLS only works practically for server-to-server communication);
* Transport layer integration for mutual TLS is impractical.

Implementers should not use both DPoP and MTLS simultaneously for sender constraining.

## Organization-Level Certificates

Some ecosystems issue certificates to organizations rather than to individual clients, for example eIDAS certificates, and an organization can operate more than one client.

NOTE: One way to distinguish a client from the organization that operates it is for each client to register the certificates and keys it uses: the subject distinguished name of its TLS client certificate using the `tls_client_auth_subject_dn` client metadata parameter [@RFC8705], and its signing keys at a `jwks_uri` [@RFC7591].

## JARM Downgrade

A client should reject the response if it requests a JARM [@JARM] response from an authorization server that advertises JARM support in its `response_modes_supported` metadata but receives the authorization response parameters, such as `code` and `state`, directly instead of in a `response` JWT.

## PKCE Downgrade

An authorization server that also serves clients that do not use PKCE [@RFC7636] can be subject to the PKCE downgrade attack described in Section 4.8 of [@RFC9700]. Section 4.8.2 of [@RFC9700] requires such an authorization server to reject a token request that contains a `code_verifier` if the authorization request did not contain a `code_challenge`.

## Native Applications

1. Clients should use the authorization code flow with redirects when the end-user uses the client and authenticates on the same device; and
2. clients should use CIBA [@CIBA] only when the end-user authenticates on an authentication device that is separate from the consumption device.

When both the client and the authorization server provide native applications, the end-user can move between them without using a browser:

1. clients should use claimed HTTPS redirect URIs as described in Section 7.2 of [@RFC8252];
2. authorization servers should claim their authorization endpoint URL in their native application; and
3. clients and authorization servers should open these URLs in the other party's application if it is installed, and in a browser otherwise.

NOTE 1: On iOS, the `universalLinksOnly` option, and on Android 11 and later, the `FLAG_ACTIVITY_REQUIRE_NON_BROWSER` intent flag, open a URL only if an installed application claims it, so that the application can fall back to a browser.

NOTE 2: On Android 12 and later, an HTTPS URL that is not a verified Android App Link always opens in a browser, so the authorization endpoint URL and redirect URI need to be verified App Links. On earlier versions, the end-user can be offered another installed application that handles the same URL.

## Access Token Size Considerations

As key size grows and more elements are added to access tokens, it's possible for the HTTP Authorization header containing the access token plus other headers to cumulatively be larger than the allowed buffer size for HTTP requests in many web infrastructure components. It is important to watch this closely via logging and alerting to ensure that production traffic is not adversely affected and that adjustments to the allowed buffer size can be made in a timely manner.

Note: While OAuth 2.0 [@RFC6749] leaves token size decisions to the authorization server, implementers should be aware that many standard web servers reject headers larger than 8KB by default.

### Security and Performance

Large access tokens can impact both security and performance:

1. Large tokens increase the risk of header-based DDOS attacks
2. Larger tokens increase network latency and resource consumption
3. Authorization servers should practice data minimization and only include necessary claims

## Key Management

Proper management of cryptographic keys is critical to the security of any FAPI 2.0 deployment. 
The compromise of private keys used for client authentication, token signing, or message signing 
can lead to severe security breaches, including unauthorized access to protected resources and 
impersonation attacks.

While detailed guidance on key management is out of scope for the FAPI specifications, 
implementers should ensure they have robust policies and procedures in place covering:

1. secure generation of cryptographic keys;
2. secure storage and protection of private keys;
3. key rotation and lifecycle management;
4. procedures for responding to key compromise;
5. access controls for key material;
6. backup and recovery procedures.

Implementers should refer to established guidance on cryptographic key management, such as 
NIST Special Publication 800-57 [@NIST.SP.800-57pt1r5] and the OWASP Key Management Cheat Sheet 
[@OWASP.KeyManagement].

NOTE: Hardware Security Modules (HSMs) or similar secure key storage mechanisms are strongly 
recommended for production deployments, particularly for high-value use cases.

## Troubleshooting Common Issues

### Connection Issues

#### Large Access Tokens

Implementers should consider logging the header size in order to catch issues with 
large access tokens or other potentially large headers.

When access tokens are too large, implementers may encounter the following symptoms:

1. HTTP 431 (Request Header Fields Too Large) responses from web servers
2. Connection resets or timeouts when making requests with large tokens
3. Inconsistent behavior where some requests succeed and others fail
4. Log entries showing truncated or malformed Authorization headers

## Authorization Server Handling of Suspicious Requests

Many Authorization Server implementations employ Web Application Firewalls (WAFs) and security rules to protect against common attacks such as XSS. This section provides guidance on balancing legitimate security concerns with the need to accept randomly generated values in parameters like state and nonce.

1. Authorization Servers may reject authorization requests that contain suspicious parameter values which could indicate malicious intent, such as potential XSS attack vectors

2. While Authorization Servers should evaluate requests for potential security issues, they should not implement blanket restrictions that block certain characters (e.g., "<") entirely

3. Authorization Servers should accept any random state/nonce values that comply with the underlying specifications

4. When rejecting suspicious requests, Authorization Servers should return or show appropriate error responses as defined in OAuth 2.0 and related specifications

5. Clients should use URL-safe characters when generating values for `state` and `nonce` parameters

6. If a client needs to include non-URL-safe characters in the `state` parameter, it should base64url encode the value, as Authorization Servers may reject values containing characters that resemble attack vectors

NOTE: What constitutes a suspicious or malicious request may vary depending on the threat model of each Authorization Server implementation. This document intentionally avoids providing an exhaustive list of patterns to block, as such a list would quickly become outdated and might provide a false sense of security.

# Acknowledgements

This document was developed by the OpenID FAPI Working Group.

{backmatter}

<reference anchor="attackermodel" target="https://openid.net/specs/fapi-attacker-model-2_0-final.html">
  <front>
    <title>FAPI 2.0 Attacker Model</title>
    <author initials="D." surname="Fett" fullname="Daniel Fett">
      <organization>Authlete</organization>
    </author>
   <date day="18" month="Feb" year="2025"/>
  </front>
</reference>

<reference anchor="CIBA" target="http://openid.net/specs/openid-client-initiated-backchannel-authentication-core-1_0.html">
    <front>
        <title>OpenID Connect Client-Initiated Backchannel Authentication Flow - Core 1.0</title>
        <author initials="G." surname="Fernandez Rodriguez" fullname="Gonzalo Fernandez Rodriguez">
            <organization>Telefonica I+D</organization>
        </author>
        <author initials="F." surname="Walter" fullname="Florian Walter">
            <organization>Deutsche Telekom AG</organization>
        </author>
        <author initials="A." surname="Nennker" fullname="Axel Nennker">
            <organization>Deutsche Telekom AG</organization>
        </author>
        <author initials="D." surname="Tonge" fullname="Dave Tonge">
            <organization>Moneyhub</organization>
        </author>
        <author initials="B." surname="Campbell" fullname="Brian Campbell">
            <organization>Ping Identity</organization>
        </author>
        <date day="1" month="September" year="2021" />
    </front>
</reference>

<reference anchor="FAPI2_Security_Profile" target="https://openid.net/specs/fapi-security-profile-2_0-final.html">
  <front>
    <title>FAPI 2.0 Security Profile</title>
    <author initials="D." surname="Fett" fullname="Daniel Fett">
      <organization>Authlete</organization>
    </author>
    <author initials="D." surname="Tonge" fullname="Dave Tonge">
      <organization>Moneyhub Financial Technology</organization>
    </author>
    <author initials="J." surname="Heenan" fullname="Joseph Heenan">
      <organization>Authlete</organization>
    </author>
   <date day="22" month="Feb" year="2025"/>
  </front>
</reference>

<reference anchor="FAPIMessageSigning" target="https://openid.net/specs/fapi-message-signing-2_0-final.html">
  <front>
    <title>FAPI 2.0 Message Signing</title>
    <author initials="D." surname="Tonge" fullname="Dave Tonge">
      <organization>Moneyhub Financial Technology</organization>
    </author>
    <author initials="D." surname="Fett" fullname="Daniel Fett">
      <organization>Authlete</organization>
    </author>
   <date day="25" month="Sep" year="2025"/>
  </front>
</reference>

<reference anchor="ISODIR2" target="https://www.iso.org/sites/directives/current/part2/index.xhtml">
<front>
<title>ISO/IEC Directives, Part 2 - Principles and rules for the structure and drafting of ISO and IEC documents</title>
    <author fullname="ISO/IEC">
      <organization>ISO/IEC</organization>
    </author>
</front>
</reference>

<reference anchor="JARM" target="https://openid.net/specs/oauth-v2-jarm-final.html">
  <front>
    <title>JWT Secured Authorization Response Mode for OAuth 2.0 (JARM)</title>
    <author initials="T." surname="Lodderstedt" fullname="Torsten Lodderstedt">
      <organization>Yes</organization>
    </author>
    <author initials="B." surname="Campbell" fullname="Brian Campbell">
      <organization>Ping</organization>
    </author>
   <date day="9" month="Nov" year="2022"/>
  </front>
</reference>

<reference anchor="NIST.SP.800-57pt1r5" target="https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final">
<front>
<title>Recommendation for Key Management: Part 1 – General</title>
    <author fullname="Elaine Barker">
      <organization>NIST</organization>
    </author>
   <date month="May" year="2020"/>
</front>
</reference>

<reference anchor="OWASP.KeyManagement" target="https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html">
<front>
<title>Key Management Cheat Sheet</title>
    <author fullname="OWASP">
      <organization>OWASP</organization>
    </author>
</front>
</reference>

# Notices

Copyright (c) 2026 The OpenID Foundation.

The OpenID Foundation (OIDF) grants to any Contributor, developer, implementer, or other interested party a non-exclusive, royalty free, worldwide copyright license to reproduce, prepare derivative works from, distribute, perform and display, this Implementers Draft, Final Specification, or Final Specification Incorporating Errata Corrections solely for the purposes of (i) developing specifications, and (ii) implementing Implementers Drafts, Final Specifications, and Final Specification Incorporating Errata Corrections based on such documents, provided that attribution be made to the OIDF as the source of the material, but that such attribution does not indicate an endorsement by the OIDF.

The technology described in this specification was made available from contributions from various sources, including members of the OpenID Foundation and others. Although the OpenID Foundation has taken steps to help ensure that the technology is available for distribution, it takes no position regarding the validity or scope of any intellectual property or other rights that might be claimed to pertain to the implementation or use of the technology described in this specification or the extent to which any license under such rights might or might not be available; neither does it represent that it has made any independent effort to identify any such rights. The OpenID Foundation and the contributors to this specification make no (and hereby expressly disclaim any) warranties (express, implied, or otherwise), including implied warranties of merchantability, non-infringement, fitness for a particular purpose, or title, related to this specification, and the entire risk as to implementing this specification is assumed by the implementer. The OpenID Intellectual Property Rights policy requires contributors to offer a patent promise not to assert certain patent claims against other contributors and against implementers. The OpenID Foundation invites any interested party to bring to its attention any copyrights, patents, patent applications, or other proprietary rights that may cover technology that may be required to practice this specification.