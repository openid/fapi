%%%
title = "FAPI 2.0 Baseline Profile"
abbrev = "fapi-2-baseline"
ipr = "none"
workgroup = "fapi"
keyword = ["security", "openid"]

[seriesInfo]
name = "Internet-Draft"
value = "fapi-2_0-baseline-01"
status = "standard"

[[author]]
initials="D."
surname="Fett"
fullname="Daniel Fett"
organization="yes.com"
    [author.address]
    email = "mail@danielfett.de"


%%%

.# Foreword

The OpenID Foundation (OIDF) promotes, protects and nurtures the OpenID community and technologies. As a non-profit international standardizing body, it is comprised by over 160 participating entities (workgroup participant). The work of preparing implementer drafts and final international standards is carried out through OIDF workgroups in accordance with the OpenID Process. Participants interested in a subject for which a workgroup has been established have the right to be represented in that workgroup. International organizations, governmental and non-governmental, in liaison with OIDF, also take part in the work. OIDF collaborates closely with other standardizing bodies in the related fields.

Final drafts adopted by the Workgroup through consensus are circulated publicly for the public review for 60 days and for the OIDF members for voting. Publication as an OIDF Standard requires approval by at least 50% of the members casting a vote. There is a possibility that some of the elements of this document may be the subject to patent rights. OIDF shall not be held responsible for identifying any or all such patent rights.

The Financial-grade API (FAPI) 2.0 Baseline profile is an API security profile
based on the OAuth 2.0 Authorization Framework [@!RFC6749]. 

.# Introduction

Financial-grade API (FAPI) 2.0 is an API security profile based on the OAuth 2.0
Authorization Framework [@!RFC6749] and related specifications suitable for
protecting APIs in high-value scenarios. While the security profile was
initially developed with a focus on financial applications, it is designed to be
universally applicable for protecting APIs exposing high-value and sensitive
(personal and other) data, for example, in e-health and e-government
applications. 

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
[@!ISODIR2]. These keywords are not used as dictionary terms such that any
occurrence of them shall be interpreted as keywords and are not to be
interpreted with their natural language meanings.

{mainmatter}

# Scope

TBD

# Terms and definitions

For the purpose of this document, the terms defined in [@!RFC6749], [@!RFC6750], [@!RFC7636], [@!OIDC] and ISO29100 apply.

# Symbols and Abbreviated terms

TBD

# Baseline Profile

## Introduction

OIDF FAPI is an API security profile based on the OAuth 2.0 Authorization
Framework [@!RFC6749]. This Baseline Profile aims to reach the security goals
laid out in the Attacker Model [@!attackermodel].

## Network Layer Protections

To protect against network attackers, clients, authorization servers, and
resource servers shall only offer TLS protected endpoints and shall establish
connections to other servers using TLS. TLS connections shall be set up to use
TLS version 1.2 or later and follow [@!RFC7525].

Endpoints for the use by web browsers shall use methods to ensure that
connections cannot be downgraded using TLS Stripping attacks. A preloaded
[@preload] HTTP Strict Transport Security policy [@!RFC6797] can be used for
this purpose. Some top-level domains, like .bank and .insurance, have set such a
policy and therefore protect all second-level domains below them.

For a comprehensive protection against network attackers, all endpoints should
additionally use DNSSEC to protect against DNS spoofing attacks that can lead to
the issuance of rogue domain-validated TLS certificates. Note: Even if an
endpoint uses only organization validated (OV) or extended validation (EV) TLS
certificates, rogue domain-validated certificates can be used to impersonate the
endpoints and conduct man-in-the-middle attacks. CAA records [@!RFC8659] can
help to mitigate this risk.

## Profile

In the following, a profile of the following technologies is defined:

  * OAuth 2.0 Authorization Framework [@!RFC6749]
  * OAuth 2.0 Bearer Tokens [@!RFC6750]
  * Proof Key for Code Exchange by OAuth Public Clients (PKCE) [@!RFC7636]
  * OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access
    Tokens (MTLS) [@!RFC8705]
  * OAuth 2.0 Demonstrating Proof-of-Possession at the Application Layer (DPoP)
    [@!I-D.ietf-oauth-dpop]
  * OAuth 2.0 Pushed Authorization Requests (PAR) [@!I-D.ietf-oauth-par]
  * OAuth 2.0 Rich Authorization Requests (RAR) [@!I-D.ietf-oauth-rar]
  * OAuth 2.0 Authorization Server Metadata [@!RFC8414]
  * OAuth 2.0 Authorization Server Issuer Identifier in Authorization Response [@!I-D.ietf-oauth-iss-auth-resp]
  * OpenID Connect Core 1.0 incorporating errata set 1 [@!OIDC]
  
### Requirements for Authorization Servers

Authorization servers

 1. shall distribute discovery metadata (such as the authorization endpoint) via
    the metadata document as specified in [@!OIDD] and [@!RFC8414]
 2. shall support the authorization code grant described in [@!RFC6749]
 3. shall reject requests using the resource owner password credentials grant or
    the implicit grant described in [@!RFC6749]
 4. shall support client-authenticated pushed authorization requests
    according to [@!I-D.ietf-oauth-par]
 5. shall reject authorization requests sent without
    [@!I-D.ietf-oauth-par]
 6. shall reject pushed authorization requests without client authentication
 7. shall support the `authorization_details` parameter according to
    [@!I-D.ietf-oauth-rar] to convey the authorization clients want to obtain if
    the `scope` parameter is not expressive enough for that purpose
 8. shall support confidential clients as defined in [@!RFC6749]
 9. shall only issue sender-constrained access tokens using one of the following
    methods:
    -  MTLS as described in [@!RFC8705]
    -  DPoP as described in [@!I-D.ietf-oauth-dpop]
 10. shall authenticate clients using one of the following methods:
     - MTLS as specified in section 2 of [@!RFC8705]
     - `private_key_jwt` as specified in section 9 of [@!OIDC]
 11. shall require PKCE [@!RFC7636] with `S256` as the code challenge method

 12. shall require the `redirect_uri` parameter in pushed authorization requests
 13. shall return an `iss` parameter in the authorization response according to
     [@!I-D.ietf-oauth-iss-auth-resp]
 14. shall not transmit authorization responses over unencrypted network
     connections, and, to this end, shall not allow redirect URIs that use the
     "http" scheme except for native clients that use Loopback Interface
     Redirection as described in [@!RFC8252], Section 7.3,
 15. shall reject an authorization code (section 1.3.1 of [@!RFC6749]) if it has
     been previously used
 16. shall provide a means for resource servers to verify the validity,
     integrity, sender-constraining, scope (incl. `authorization_details`),
     expiration and revocation status of an access token, either by providing an
     introspection endpoint [@!RFC7662], by exposing signature verification
     keys, or by deployment-specific means.
 17. shall not use the HTTP 307 status code when redirecting a request that contains 
     user credentials to avoid forwarding the credentials to a third party accidentally 
     (see section 4.11 of [I-D.ietf-oauth-security-topics]); 
 18. should use the HTTP 303 status code when redirecting the user agent using status codes;
 19. shall not expose open redirectors (see section 4.10 of
     [@I-D.ietf-oauth-security-topics])
 19. shall accept its issuer identifier value (as defined in [@RFC8414]) in the `aud` claim 
     received in client authentication assertions.
 
**NOTE**: In order to facilitate interoperability the authorization server should also 
accept  its token endpoint URL or the URL of the endpoint at which the assertion was 
received in the `aud` claim received in client authentication assertions.

**NOTE**: If replay identification of the authorization code is not possible, it
is desirable to set the validity period of the authorization code to one minute
or a suitable short period of time. The validity period may act as a cache
control indicator of when to clear the authorization code cache if one is used.

**NOTE**: To enable an interoperable solution to consent management it is anticipated that 
future versions of this specification will reference the FAPI WG's Grant Management API. 
#### Returning Authenticated User's Identifier

If it is desired to provide the authenticated user's identifier to the client in
the token response, the authorization server shall support OpenID Connect
[@!OIDC].

### Requirements for Clients

Clients

 1. shall use the authorization code grant described in [@!RFC6749]
 2. shall use pushed authorization requests according to [@!I-D.ietf-oauth-par]
 3. shall support sender-constrained access tokens using one of the following methods:
    -  MTLS as described in [@!RFC8705]
    -  DPoP as described in [@!I-D.ietf-oauth-dpop]
 4. shall support client authentication using one of the following methods:
    - MTLS as specified in section 2 of [@!RFC8705]
    - `private_key_jwt` as specified in section 9 of [@!OIDC]
 5. shall use PKCE [@!RFC7636] with `S256` as the code challenge method
 6. shall send access tokens in the HTTP header as in Section 2.1 of OAuth 2.0
    Bearer Token Usage [@!RFC6750]
 7. shall check the `iss` parameter in the authorization response according to
    [@!I-D.ietf-oauth-iss-auth-resp] to prevent Mix-Up attacks
 8. shall not expose open redirectors (see section 4.10 of
     [@I-D.ietf-oauth-security-topics])
 9. if using `private_key_jwt`, shall use the Authorization Server's issuer identifier 
    value (as defined in [@RFC8414]) in the `aud` claim sent in client authentication assertions. 
    The issuer identifier value shall be sent as a string not as an item in an array.

### Requirements for Resource Servers

The FAPI 2.0 endpoints are OAuth 2.0 protected resource endpoints that return
protected information for the resource owner associated with the submitted
access token.

Resource servers with the FAPI endpoints

1. shall accept access tokens in the HTTP header as in Section 2.1 of OAuth 2.0
   Bearer Token Usage [@!RFC6750]
1. shall not accept access tokens in the query parameters stated in Section 2.3
   of OAuth 2.0 Bearer Token Usage [@!RFC6750]
1. shall verify the validity, integrity, expiration and revocation status of
   access tokens
1. shall verify that the scope (incl. `authorization_details`) of the access
   token authorizes the access to the resource it is representing
1. shall support and verify sender-constrained access tokens using one of the following methods:
    -  MTLS as described in [@!RFC8705]
    -  DPoP as described in [@!I-D.ietf-oauth-dpop]
2. shall identify the associated entity to the access token
3. shall only return the resource identified by the combination of the entity
   implicit in the access and the granted scope and otherwise return errors as
   in section 3.1 of [@!RFC6750]


## Cryptography and Secrets

 
 1. Authorization Servers, Clients, and Resource Servers shall adhere to
    [@!RFC8725] when creating or processing JWTs. In particular,
     * the algorithm-specific recommendations in Section 3.2 shall be followed,
     * and the `none` algorithm shall not be used or accepted.
 2. RSA keys shall have a minimum length of 2048 bits.
 3. Elliptic curve keys shall have a minimum length of 160 bits.
 4. Credentials not intended for handling by end-users (e.g., access tokens,
    refresh tokens, authorization codes, etc.) shall be created with at least
    128 bits of entropy such that an attacker correctly guessing the value is
    computationally infeasible. Cf. Section 10.10 of  [@!RFC6749].


## Differences to FAPI 1.0

| FAPI 1.0 Read/Write                      | FAPI 2.0                            | Reasons                                                                                               |
| :--------------------------------------- | :---------------------------------- | :---------------------------------------------------------------------------------------------------- |
| JAR, JARM                                | PAR                                 | integrity protection and compatibility improvements for authorization requests; only code in response |
| -                                        | RAR                                 | support complex and structured information about authorizations                                       |
| -                                        | shall adhere to Security BCP        |                                                                                                       |
| `s_hash`                                 | -                                   | state integrity is protected by PAR; protection provided by state is now provided by PKCE             |
| pre-registered redirect URIs             | redirect URIs in PAR                | pre-registration is not required with client authentication and PAR                                   |
| response types `code id_token` or `code` | response type `code`                | improve security: no ID token in front-channel; not needed                                            |
| ID Token as detached signature           | -                                   | ID token does not need to serve as a detached signature                                               |
| signed and encrypted ID Tokens           | signing and encryption not required | ID Tokens only exchanged in back channel                                                              |
| `exp` claim in request object            | -                                   | ?                                                                                                     |
| `x-fapi-*` headers                       | -                                   | Removed pending further discussion                                                                    |
| MTLS for sender-constrained access tokens | MTLS or DPoP                                             |                                                                                                       |

# Security considerations

TBD

# Privacy considerations

TBD

# Acknowledgements

We would like to thank Takahiko Kawasaki, Filip Skokan, Dave Tonge, Nat Sakimura, Stuart Low, Dima Postnikov, Torsten Lodderstedt, Joseph Heenan, Travis Spencer, Brian Campbell, Ralph Bragg and Lukasz Jaromin for their valuable feedback and contributions that helped to evolve this specification.

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

<reference anchor="OIDC" target="http://openid.net/specs/openid-connect-core-1_0.html">
  <front>
    <title>OpenID Connect Core 1.0 incorporating errata set 1</title>
    <author initials="N." surname="Sakimura" fullname="Nat Sakimura">
      <organization>NRI</organization>
    </author>
    <author initials="J." surname="Bradley" fullname="John Bradley">
      <organization>Ping Identity</organization>
    </author>
    <author initials="M." surname="Jones" fullname="Mike Jones">
      <organization>Microsoft</organization>
    </author>
    <author initials="B." surname="de Medeiros" fullname="Breno de Medeiros">
      <organization>Google</organization>
    </author>
    <author initials="C." surname="Mortimore" fullname="Chuck Mortimore">
      <organization>Salesforce</organization>
    </author>
   <date day="8" month="Nov" year="2014"/>
  </front>
</reference>

<reference anchor="OIDD" target="https://openid.net/specs/openid-connect-discovery-1_0.html">
  <front>
    <title>OpenID Connect Discovery 1.0 incorporating errata set 1</title>
    <author initials="N." surname="Sakimura" fullname="Nat Sakimura">
      <organization>NRI</organization>
    </author>
    <author initials="J." surname="Bradley" fullname="John Bradley">
      <organization>Ping Identity</organization>
    </author>
    <author initials="M." surname="Jones" fullname="Mike Jones">
      <organization>Microsoft</organization>
    </author>
    <author initials="E." surname="Jay" fullname="Edmund Jay">
      <organization>Illumila</organization>
    </author>
    <date day="8" month="Nov" year="2014"/>
  </front>
</reference>


<reference anchor="preload" target="https://hstspreload.org/">
<front>
<title>HSTS Preload List Submission</title>
    <author fullname="Anonymous">
      <organization></organization>
    </author>
</front>
</reference>


<reference anchor="ISODIR2" target="https://www.iso.org/sites/directives/current/part2/index.xhtml">
<front>
<title>ISO/IEC Directives Part 2 - </title>
    <author fullname="International Organization for Standardization">
      <organization></organization>
    </author>
</front>
</reference>

# Notices

Copyright (c) 2021 The OpenID Foundation.

The OpenID Foundation (OIDF) grants to any Contributor, developer, implementer, or other interested party a non-exclusive, royalty free, worldwide copyright license to reproduce, prepare derivative works from, distribute, perform and display, this Implementers Draft or Final Specification solely for the purposes of (i) developing specifications, and (ii) implementing Implementers Drafts and Final Specifications based on such documents, provided that attribution be made to the OIDF as the source of the material, but that such attribution does not indicate an endorsement by the OIDF.

The technology described in this specification was made available from contributions from various sources, including members of the OpenID Foundation and others. Although the OpenID Foundation has taken steps to help ensure that the technology is available for distribution, it takes no position regarding the validity or scope of any intellectual property or other rights that might be claimed to pertain to the implementation or use of the technology described in this specification or the extent to which any license under such rights might or might not be available; neither does it represent that it has made any independent effort to identify any such rights. The OpenID Foundation and the contributors to this specification make no (and hereby expressly disclaim any) warranties (express, implied, or otherwise), including implied warranties of merchantability, non-infringement, fitness for a particular purpose, or title, related to this specification, and the entire risk as to implementing this specification is assumed by the implementer. The OpenID Intellectual Property Rights policy requires contributors to offer a patent promise not to assert certain patent claims against other contributors and against implementers. The OpenID Foundation invites any interested party to bring to its attention any copyrights, patents, patent applications, or other proprietary rights that may cover technology that may be required to practice this specification.