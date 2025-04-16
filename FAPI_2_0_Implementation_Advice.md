%%%
title = "FAPI 2.0 Implementation Advice"
abbrev = "fapi-2-implementation-advice"
ipr = "none"
workgroup = "connect"
keyword = ["security", "openid"]

[seriesInfo]
name = "Internet-Draft"
value = "fapi-2_0-implementation_advice-01"
status = "standard"

[[author]]
initials="D."
surname="Tonge"
fullname="Dave Tonge"
organization="Moneyhub"
    [author.address]
    email = "dave@tonge.org"


%%%

.# Abstract 

Financial-grade API (FAPI) 2.0 Implementation Advice is a document to provide practical
guidance on the implementation and usage of the FAPI 2.0 family of standards.

{mainmatter}

# Introduction

The Financial-grade API (FAPI) 2.0 family of standards provides security profiles and specifications
to enable implementers to deploy highly secure, interoperable APIs. While we have attempted 
to minimize the optionality in FAPI 2.0, there are still many decisions that need to be made by
implementers. This document aims to provide advice for implementers based on the experience
of members of the OpenID Foundation's FAPI Working Group.

## Warning

This document is not an OIDF International Standard. It is distributed for
review and comment. It is subject to change without notice and may not be
referred to as an International Standard.

Recipients of this draft are invited to submit, with their comments,
notification of any relevant patent rights of which they are aware and to
provide supporting documentation.

## Copyright notice & license

The OpenID Foundation (OIDF) grants to any Contributor, developer, implementer,
or other interested party a non-exclusive, royalty free, worldwide copyright
license to reproduce, prepare derivative works from, distribute, perform and
display, this Implementers Draft or Final Specification solely for the purposes
of (i) developing specifications, and (ii) implementing Implementers Drafts and
Final Specifications based on such documents, provided that attribution be made
to the OIDF as the source of the material, but that such attribution does not
indicate an endorsement by the OIDF.

The technology described in this specification was made available from
contributions from various sources, including members of the OpenID Foundation
and others. Although the OpenID Foundation has taken steps to help ensure that
the technology is available for distribution, it takes no position regarding the
validity or scope of any intellectual property or other rights that might be
claimed to pertain to the implementation or use of the technology described in
this specification or the extent to which any license under such rights might or
might not be available; neither does it represent that it has made any
independent effort to identify any such rights. The OpenID Foundation and the
contributors to this specification make no (and hereby expressly disclaim any)
warranties (express, implied, or otherwise), including implied warranties of
merchantability, non-infringement, fitness for a particular purpose, or title,
related to this specification, and the entire risk as to implementing this
specification is assumed by the implementer. The OpenID Intellectual Property
Rights policy requires contributors to offer a patent promise not to assert
certain patent claims against other contributors and against implementers. The
OpenID Foundation invites any interested party to bring to its attention any
copyrights, patents, patent applications, or other proprietary rights that may
cover technology that may be required to practice this specification.

## Notational Conventions

The keywords "shall", "shall not", "should", "should not", "may", and "can" in
this document are to be interpreted as described in ISO Directive Part 2
[@ISODIR2]. These keywords are not used as dictionary terms such that any
occurrence of them shall be interpreted as keywords and are not to be
interpreted with their natural language meanings.

# Implementation Advice

## FAPI 2.0 Framework

The FAPI 2.0 Framework is comprised of several documents. At the time of writing, they are:

* FAPI 2.0 Attacker model;
* FAPI 2.0 Security profile;
* FAPI 2.0 Message signing - for non repudiation of messages;
* FAPI Client Initiated Backchannel Authentication - for decoupled or cross device flows;
* Grant Management for OAuth 2.0 - for ecosystems that require interoperable grant management;
* OAuth 2.0 Rich Authorization Requests  - for conveying complex authorizations.

The foundation of the framework is the attacker model and security profile. All the other 
specifications build on the security profile.

## HTTP Headers

Implementers may find the following http-headers useful:

### x-fapi-interaction-id

This header can be used to enable Authorization Servers, Resource Servers and Clients to
better track and debug any issues between them. If an ecosystem adopts `x-fapi-interaction-id` then 
the following clauses apply:


1. clients shall send the `x-fapi-interaction-id` request header, the value shall be a 
RFC4122 UUID,  e.g., `x-fapi-interaction-id: c770aef3-6784-41f7-8e0e-ff5f97bddb3a`;
1. the AS or RS shall set the response header `x-fapi-interaction-id` to the value received from the corresponding FAPI client request header or to a [RFC4122] UUID value if the request header was not provided to track the interaction, e.g., `x-fapi-interaction-id: c770aef3-6784-41f7-8e0e-ff5f97bddb3a`;
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

## Access Token Size Considerations

As key size grows and more elements are added to access tokens, it's possible for the HTTP Authorization header containing the access token plus other headers to cumulatively be larger than the allowed buffer size for HTTP requests in many web infrastructure components. It is important to watch this closely via logging and alerting to ensure that production traffic is not adversely affected and that adjustments to the allowed buffer size can be made in a timely manner.

Note: While OAuth 2.0 [@RFC6749] leaves token size decisions to the authorization server, implementers should be aware that many standard web servers reject headers larger than 8KB by default.

### Security and Performance

Large access tokens can impact both security and performance:

1. Large tokens increase the risk of header-based DDOS attacks
2. Larger tokens increase network latency and resource consumption
3. Authorization servers should practice data minimization and only include necessary claims

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

## Acknowledgements

todo...

{backmatter}

<reference anchor="attackermodel" target="https://bitbucket.org/openid/fapi/src/master/FAPI_2_0_Attacker_Model.md">
  <front>
    <title>FAPI 2.0 Attacker Model</title>
    <author initials="D." surname="Fett" fullname="Daniel Fett">
      <organization>yes.com</organization>
    </author>
   <date day="28" month="Jul" year="2021"/>
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

# Notices

Copyright (c) 2021 The OpenID Foundation.

The OpenID Foundation (OIDF) grants to any Contributor, developer, implementer, or other interested party a non-exclusive, royalty free, worldwide copyright license to reproduce, prepare derivative works from, distribute, perform and display, this Implementers Draft or Final Specification solely for the purposes of (i) developing specifications, and (ii) implementing Implementers Drafts and Final Specifications based on such documents, provided that attribution be made to the OIDF as the source of the material, but that such attribution does not indicate an endorsement by the OIDF.

The technology described in this specification was made available from contributions from various sources, including members of the OpenID Foundation and others. Although the OpenID Foundation has taken steps to help ensure that the technology is available for distribution, it takes no position regarding the validity or scope of any intellectual property or other rights that might be claimed to pertain to the implementation or use of the technology described in this specification or the extent to which any license under such rights might or might not be available; neither does it represent that it has made any independent effort to identify any such rights. The OpenID Foundation and the contributors to this specification make no (and hereby expressly disclaim any) warranties (express, implied, or otherwise), including implied warranties of merchantability, non-infringement, fitness for a particular purpose, or title, related to this specification, and the entire risk as to implementing this specification is assumed by the implementer. The OpenID Intellectual Property Rights policy requires contributors to offer a patent promise not to assert certain patent claims against other contributors and against implementers. The OpenID Foundation invites any interested party to bring to its attention any copyrights, patents, patent applications, or other proprietary rights that may cover technology that may be required to practice this specification.