%%%
title = "FAPI 2.0 Security Profile — draft"
abbrev = "fapi-2-security-profile"
ipr = "none"
workgroup = "fapi"
keyword = ["security", "openid"]

[seriesInfo]
name = "Internet-Draft"
value = "fapi-2_0-security-profile-03"
status = "standard"

[[author]]
initials="D."
surname="Fett"
fullname="Daniel Fett"
organization="Authlete"
    [author.address]
    email = "mail@danielfett.de"

[[author]]
initials="D."
surname="Tonge"
fullname="Dave Tonge"
organization="Moneyhub Financial Technology"
    [author.address]
    email = "dave@tonge.org"

[[author]]
initials="J."
surname="Heenan"
fullname="Joseph Heenan"
organization="Authlete"
    [author.address]
    email = "joseph@authlete.com"


%%%

.# Foreword

The OpenID Foundation (OIDF) promotes, protects and nurtures the OpenID community and technologies. As a non-profit international standardizing body, it is comprised by over 160 participating entities (workgroup participant). The work of preparing implementer drafts and final international standards is carried out through OIDF workgroups in accordance with the OpenID Process. Participants interested in a subject for which a workgroup has been established have the right to be represented in that workgroup. International organizations, governmental and non-governmental, in liaison with OIDF, also take part in the work. OIDF collaborates closely with other standardizing bodies in the related fields.

Final drafts adopted by the Workgroup through consensus are circulated publicly for the public review for 60 days and for the OIDF members for voting. Publication as an OIDF Standard requires approval by at least 50% of the members casting a vote. There is a possibility that some of the elements of this document may be subject to patent rights. OIDF shall not be held responsible for identifying any or all such patent rights.


.# Introduction

The FAPI 2.0 Security Profile is an API security profile based on the
OAuth 2.0 Authorization Framework [@!RFC6749] and related specifications suitable for
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
[@ISODIR2]. These keywords are not used as dictionary terms such that any
occurrence of them shall be interpreted as keywords and are not to be
interpreted with their natural language meanings.

{mainmatter}

# Scope

This specification is a general-purpose high security profile of
OAuth 2.0 that has been proved by formal analysis to meet the stated
attacker model. This document specifies the requirements for:

 - Confidential Clients to securely obtain OAuth tokens from Authorization Servers;
 - Confidential Clients to securely use those tokens to access protected resources at Resource Servers;
 - Authorization Servers to securely issue OAuth tokens to confidential Clients;
 - Resource Servers to securely accept and verify OAuth tokens from confidential Clients.

# Normative references
The following documents are referred to in the text in such a way that some or all of their content constitutes requirements of this document. For dated references, only the edition cited applies. For undated references, the latest edition of the referenced document (including any amendments) applies.

See Section 8 for normative references.

# Terms and definitions

For the purpose of this document, the terms defined in [@!RFC6749], [@!RFC6750], [@!RFC7636], [@!OIDC] and [@!ISO29100] apply.

# Symbols and Abbreviated terms

**API** – Application Programming Interface

**HTTP** – Hyper Text Transfer Protocol

**REST** – Representational State Transfer

**TLS** – Transport Layer Security

**DNS** - Domain Name System

**DNSSEC** -  Domain Name System Security Extensions

**CAA** - Certificate Authority Authorization

**URI** - Uniform Resource Identifier

# Security Profile

## Overview

### Introduction

The FAPI 2.0 Security Profile is an API security profile based on the OAuth 2.0 Authorization
Framework [@!RFC6749], that aims to reach the security goals laid out in the Attacker
Model [@!attackermodel].

This profile is the base of the FAPI 2.0 Framework. Other specifications that are
part of this framework and may be used together with this profile include:

1. FAPI Message Signing [@FAPIMessageSigning] is recommended when messages are required to be signed for the
   purposes of non-repudiation.
1. FAPI Client Initiated Backchannel Authentication [@FAPICIBA] is recommended when support is
   required for decoupled or cross device flows.
1. Grant Management [@GrantManagement] is recommended for ecosystems that require interoperable grant management.
1. OAuth 2.0 Rich Authorization Requests (RAR) [@RFC9396] is recommended when
   the `scope` parameter is not expressive enough to convey the authorization that a client
   wants to obtain.

The OpenID FAPI Working Group is not currently aware of any mechanisms that would allow public clients
to be secured to the same degree and hence their use is not within the scope
of this specification.

Although it is possible to code Authorization Servers and Clients from first
principles using this specification, implementers are encouraged to build on top
of existing OpenID Connect and/or OAuth 2 implementations instead of embarking
on a 'from scratch' implementation. See
(#incomplete-or-incorrect-implementations-of-the-specifications) for additional
considerations for ensuring that implementations are complete and correct.

### Profiling this specification

This specification is a general purpose high security profile of
OAuth 2.0 that has been proved by formal analysis to meet the stated
attacker model.

This specification, and the underlying specifications, leave a number
of choices open to implementors, deployers and/or ecosystems. With
knowledge of the exact use cases, further reducing the number of
choices may further improve security, or make implementation or
interoperability easier.

However, for a profile to be compliant with this specification, the
profile shall not remove or override mandatory behaviors, as doing
so is likely to invalidate the formal security analysis and reduce
security in potentially unpredictable ways.

## Network Layer Protections

### Requirements for all endpoints

All TLS connections between web browsers, clients, authorization
servers, and resource servers shall be protected against network
attackers. To this end, clients, authorization servers, and resource
servers

 1. shall only offer TLS protected endpoints and shall establish connections
    to other servers using TLS;
 1. shall set up TLS connections using TLS version 1.2 or later;
 2. when using TLS 1.2, shall follow the recommendations for Secure Use of Transport Layer Security in [@!BCP195];
 3. should use DNSSEC to protect against DNS spoofing attacks that can lead to
    the issuance of rogue domain-validated TLS certificates; and
 4. shall perform a TLS server certificate check, as per [@!RFC6125].

**NOTE 1**: Even if an endpoint uses only organization validated (OV) or extended
validation (EV) TLS certificates, an attacker using rogue domain-validated
certificates is able to impersonate the endpoint and conduct man-in-the-middle
attacks. CAA records [@!RFC8659] can help to mitigate this risk.

### Requirements for endpoints not used by web browsers

For server-to-server communication endpoints that are not used by web
browsers, the following requirements apply:

 1. When using TLS 1.2, servers shall only permit the cipher suites listed in (#tls-12-ciphers).
 2. When using TLS 1.2, clients should only permit the cipher suites listed in (#tls-12-ciphers).
 3. When using the `TLS_DHE_RSA_WITH_AES_128_GCM_SHA256` or `TLS_DHE_RSA_WITH_AES_256_GCM_SHA384` cipher suites,
 key lengths of at least 2048 bits are required.

#### TLS 1.2 permitted cipher suites {#tls-12-ciphers}

For TLS 1.2, only the following cipher suites shall be used:

  * `TLS_DHE_RSA_WITH_AES_128_GCM_SHA256`
  * `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256`
  * `TLS_DHE_RSA_WITH_AES_256_GCM_SHA384`
  * `TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384`

### Requirements for endpoints used by web browsers

For endpoints that are used by web browsers, the following additional
requirements apply:

  1. Servers shall use methods to ensure that connections cannot be
     downgraded using TLS Stripping attacks. A preloaded [@preload] HTTP
     Strict Transport Security policy [@!RFC6797] can be used for this
     purpose. Some top-level domains, like `.bank` and `.insurance`,
     have set such a policy and therefore protect all second-level
     domains below them.
  2. When using TLS 1.2, servers shall only use cipher suites allowed in
     [@!BCP195].

## Profile

### General

In the following, a profile of the following technologies is defined:

  * OAuth 2.0 Authorization Framework [@!RFC6749]
  * OAuth 2.0 Bearer Tokens [@!RFC6750]
  * Proof Key for Code Exchange by OAuth Public Clients (PKCE) [@!RFC7636]
  * OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access
    Tokens (MTLS) [@!RFC8705]
  * OAuth 2.0 Demonstrating Proof of Possession (DPoP)
    [@!RFC9449]
  * OAuth 2.0 Pushed Authorization Requests (PAR) [@!RFC9126]
  * OAuth 2.0 Authorization Server Metadata [@!RFC8414]
  * OAuth 2.0 Authorization Server Issuer Identification [@!RFC9207]
  * OpenID Connect Core 1.0 incorporating errata set 1 [@!OIDC]

### Requirements for Authorization Servers

#### General Requirements

Authorization servers

 1. shall distribute discovery metadata (such as the authorization endpoint) via
    the metadata document as specified in [@!OIDD] and [@!RFC8414];
 1. shall reject requests using the resource owner password credentials grant;
 1. shall only support confidential clients as defined in [@!RFC6749];
 1. shall only issue sender-constrained access tokens;
 1. shall use one of the following methods for sender-constrained access tokens:
    -  MTLS as described in [@!RFC8705],
    -  DPoP as described in [@!RFC9449];
 1. shall authenticate clients using one of the following methods:
     - MTLS as specified in Section 2 of [@!RFC8705], or
     - `private_key_jwt` as specified in Section 9 of [@!OIDC];
 1. shall not expose open redirectors (see Section 4.10 of
     [@I-D.ietf-oauth-security-topics]);
 1. shall accept its issuer identifier value (as defined in [@RFC8414]) either as the
    `aud` claim (when a string) or as a member of the `aud` claim (when an array) received
    in client authentication assertions;
 1. should accept its token endpoint url or the url of the endpoint at which the
    assertion was received, either as the `aud` claim (when a string) or as a member
    of the `aud` claim (when an array) received in client authentication assertions;
 1. shall not use refresh token rotation unless, in the case a response with a new
     refresh token is not received and stored by the client, retrying the request (with
     the previous refresh token) will succeed;
 1. if using DPoP, may use the server provided nonce mechanism (as defined in Section 8 of [@!RFC9449]);
 1. shall issue authorization codes with a maximum lifetime of 60 seconds;
 1. if using DPoP, shall support "Authorization Code Binding to DPoP Key" (as required by Section 10.1 of [@!RFC9449]); and
 1. to accommodate for clock offsets, shall accept JWTs with an `iat` or `nbf` time up to 10 seconds in the future, however should reject JWTs with an `iat` or `nbf` of 60 seconds or greater in the future.

**NOTE 1**:
To facilitate interoperability, this document requires that Authorization Servers
accept their issuer value in the `aud` claim received in client authentication
assertions. It recommends that they also accept their token endpoint url or the url
of the endpoint at which the assertion was received. This does not reduce the stricter
requirement in [@!RFC9126] that requires all 3 values to be accepted at the PAR endpoint.

**NOTE 2**:
Refresh token rotation is an optional feature defined in Section 6 of [@!RFC6749]
where the Authorization Server issues a new refresh token to the client as part of the
`refresh_token` grant. This specification discourages the use of this feature as it
does not bring any security benefits for confidential clients, and can cause significant
operational issues. However, to allow for operational agility, Authorization Servers
may implement it providing they meet the requirement in Clause 9.

**NOTE 3**:
This document is structured to support a variety of grants to be used with the general
requirements above. For example the client credentials grant or the FAPI CIBA grant. Implementers
should note that as of the time of writing only the Authorization Code flow and CIBA flows have
been through a detailed security analysis.

**NOTE 4**:
DPoP already suggests that JWTs are accepted in the reasonably near future (on the order of seconds or minutes).
This specification goes further by placing a hard lower bound of 10 seconds in order to promote interoperability.


#### Authorization Endpoint Flows

For flows that use the authorization endpoint, Authorization Servers

1. shall require the value of `response_type` described in [@!RFC6749] to be `code`;
1. shall support client-authenticated pushed authorization requests
    according to [@!RFC9126];
1. shall reject authorization requests sent without [@!RFC9126];
1. shall reject pushed authorization requests without client authentication;
1. shall require PKCE [@!RFC7636] with `S256` as the code challenge method;
1. shall require the `redirect_uri` parameter in pushed authorization requests;
1. shall return an `iss` parameter in the authorization response according to [@!RFC9207];
1. shall not transmit authorization responses over unencrypted network
     connections, and, to this end, shall not allow redirect URIs that use the
     "http" scheme except for native clients that use Loopback Interface
     Redirection as described in Section 7.3 of [@!RFC8252];
1. shall reject an authorization code (Section 1.3.1 of [@!RFC6749]) if it has
     been previously used;
1. shall not use the HTTP 307 status code when redirecting a request that contains
     user credentials to avoid forwarding the credentials to a third party accidentally
     (see Section 4.11 of [I-D.ietf-oauth-security-topics]);
1. should use the HTTP 303 status code when redirecting the user agent using status codes;
1. shall issue pushed authorization requests `request_uri` with `expires_in` values
     of less than 600 seconds; and
1. should provide End-Users with all necessary information to make an
   informed decision about whether to consent to the authorization
   request, including the identity of the client and the scope of the
   authorization.


**NOTE 1**:
If replay identification of the authorization code is not possible, it
is desirable to set the validity period of the authorization code to one minute
or a suitable short period of time. The validity period may act as a cache
control indicator of when to clear the authorization code cache if one is used.

**NOTE 2**:
The `request_uri` `expires_in` time must be sufficient for
the user's device to receive the link and the user to complete the
process of opening the link. In many cases (poor network connection or
where the user has to manually select the browser to be used) this can
easily take over 30 seconds. 

**NOTE**: It is recommended that Authorization Servers that enforce one-time 
use of `request_uri` values ensure the enforcement takes place at 
the point of authorization, not at the point of loading an authorization page. 
This prevents user software that preloads urls from invalidating the 
`request_uri`.

#### Returning Authenticated User's Identifier

If it is desired to provide the authenticated user's identifier to the client in
the token response, the authorization server shall support OpenID Connect
[@!OIDC].

### Requirements for Clients

#### General Requirements

Clients

 1. shall support sender-constrained access tokens using one or both of the following methods:
    -  MTLS as described in [@!RFC8705],
    -  DPoP as described in [@!RFC9449];
 1. shall support client authentication using one or both of the following methods:
    - MTLS as specified in Section 2 of [@!RFC8705],
    - `private_key_jwt` as specified in Section 9 of [@!OIDC];
 1. shall send access tokens in the HTTP header as in Section 2.1 of OAuth 2.0
    Bearer Token Usage [@!RFC6750];
 1. shall not expose open redirectors (see Section 4.10 of
     [@I-D.ietf-oauth-security-topics]);
 1. if using `private_key_jwt`, shall use the Authorization Server's
    issuer identifier value (as defined in [@RFC8414]) in the `aud`
    claim in client authentication assertions, and should send the issuer
    identifier value as a string, not as an item in an
    array;
 1. shall support refresh tokens and their rotation;
 1. if using MTLS client authentication or MTLS sender-constrained access tokens, shall support
    the `mtls_endpoint_aliases` metadata defined in [@!RFC8705];
 1. if using DPoP, shall support the server provided nonce mechanism (as defined in Section 8 of [@!RFC9449]);
 1. shall only use authorization server metadata (such as the authorization endpoint) retrieved from the metadata document as specified in [@!OIDD] and [@!RFC8414];
 1. shall ensure that the issuer URL used as the basis for retrieving the authorization server metadata is obtained from an authoritative source and using a secure channel, such that it cannot be modified by an attacker;
 1. shall ensure that this issuer URL and the `issuer` value in the obtained metadata match; and
 1. shall initiate an authorization process only with the End-User's
    explicit or implicit consent and protect initiation of an
    authorization process against Cross-Site Request Forgery, thereby
    enabling the End-User to be aware of the context in which a flow was
    started.

**NOTE 1**:
This profile may be used by Confidential Clients on a user-controlled device where the system
clock may not be accurate, causing `private_key_jwt` client authentication to fail.
In such circumstances a Client should consider using the HTTP Date header returned from the
server to synchronize its own clock when generating client assertions.

**NOTE 2**:
Although Authorization Servers are required to support "Authorization
Code Binding to DPoP Key" (as defined by Section 10.1 of
[@!RFC9449]), clients are not required to use it.


#### Authorization Code Flow

For the Authorization Code flow, Clients

 1. shall use the authorization code grant described in [@!RFC6749];
 1. shall use pushed authorization requests according to [@!RFC9126];
 1. shall use PKCE [@!RFC7636] with `S256` as the code challenge method;
 1. shall check the `iss` parameter in the authorization response according to [@!RFC9207] to prevent Mix-Up attacks; and
 1. shall only send `client_id` and `request_uri` request parameters to the authorization endpoint (all other authorization request parameters are sent in the pushed authorization request according to [@!RFC9126]).

### Requirements for Resource Servers

The FAPI 2.0 endpoints are OAuth 2.0 protected resource endpoints that return
protected information for the resource owner associated with the submitted
access token.

Resource servers with the FAPI endpoints

1. shall accept access tokens in the HTTP header as in Section 2.1 of OAuth 2.0
   Bearer Token Usage [@!RFC6750];
1. shall not accept access tokens in the query parameters stated in Section 2.3
   of OAuth 2.0 Bearer Token Usage [@!RFC6750];
1. shall verify the validity, integrity, expiration and revocation status of
   access tokens;
1. shall verify that the authorization represented by the access token is sufficient
   for the requested resource access and otherwise return errors as in Section 3.1
   of [@!RFC6750]; and
1. shall support and verify sender-constrained access tokens using one or both of the following methods:
    -  MTLS as described in [@!RFC8705],
    -  DPoP as described in [@!RFC9449].


## Cryptography and Secrets

The following requirements apply to cryptographic operations and secrets:

 1. Authorization Servers, Clients, and Resource Servers when creating or processing JWTs shall

    1. adhere to [@!RFC8725];
    2. use `PS256`, `ES256`, or `EdDSA` (using the `Ed25519` subtype) algorithms; and
    3. not use or accept the `none` algorithm.

 2. RSA keys shall have a minimum length of 2048 bits.
 3. Elliptic curve keys shall have a minimum length of 160 bits.
 4. Credentials not intended for handling by End-Users (e.g., access tokens,
    refresh tokens, authorization codes, etc.) shall be created with at least
    128 bits of entropy such that an attacker correctly guessing the value is
    computationally infeasible. Cf. Section 10.10 of [@!RFC6749].

## MTLS Protection of all endpoints

Some ecosystems are choosing to require clients accessing their endpoints to supply a TLS client certificate at
endpoints that would not otherwise require a TLS client certificate (for example, the PAR endpoint when using
`private_key_jwt` authentication).

This is outside of the scope of both [@!RFC8705] and the FAPI standards, however in the interests of interoperability
this document states that when using TLS as a transport level protection in this manner, authorization servers should
expect clients to call the endpoints located in the root of the server metadata, and not those found in
`mtls_endpoint_aliases`.


## Main Differences to FAPI 1.0

| FAPI 1.0 Read/Write                                  | FAPI 2.0                                                                   | Reasons                                                                                                                                 |
| :--------------------------------------------------- | :------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| JAR                                                  | PAR                                                                        | integrity protection and compatibility improvements for authorization requests                                                          |
| JARM                                                 | only code in response                                                      | the authorization response is reduced to only contain the authorization code, obsoleting the need for integrity protection              |
| BCM principles, defences based on particular threats | attacker model, security goals, best practices from the OAuth Security BCP | clearer design guideline, suitability for formal analysis                                                                               |
| `s_hash`                                             | PKCE                                                                       | protection provided by `state` (in particular against CSRF) is now provided by PKCE; `state` integrity is partially protected by PAR    |
| pre-registered redirect URIs                         | redirect URIs in PAR                                                       | pre-registration is not required with client authentication and PAR                                                                     |
| response types `code id_token` or `code`             | response type `code`                                                       | no ID token in front-channel (privacy improvement); nonce/signature check can be skipped by clients, PKCE cannot (security improvement) |
| ID Token as detached signature                       | PKCE                                                                       | ID token does not need to serve as a detached signature                                                                                 |
| potentially encrypted ID Tokens in the front channel | No encryption and no ID Tokens in the front channel                        | ID Tokens only exchanged in back channel                                                                                                |
| `nbf` & `exp` claims in request object               | `request_uri` has limited lifetime                                         | Prevents pre-generation of requests                                                                                                     |
| `x-fapi-*` headers                                   | Moved to Implementation and Deployment Advice document                     | Not relevant to the core of the security profile                                                                                        |
| MTLS for sender-constrained access tokens            | MTLS or DPoP                                                               | Due to the lack of the tight integration with the TLS layer, DPoP can be easier to deploy in some scenarios                             |

## Security Considerations

### Access token lifetimes

The use of short-lived access tokens (combined with refresh tokens) potentially reduces the time window for some attacks.

The use of refresh tokens also allows clients to rotate their sender-constraining keys without loss of grants, either because of compromise of the key or as part of good security hygiene.

If issuing long-lived grants (e.g. days/weeks), the use of short-lived (e.g. minutes/hours) access tokens combined with refresh tokens should be considered.

There is a performance and resiliency trade-off, setting the access token lifetime too short can increase the load on and dependency on the authorization server.

### DPoP Proof Replay

An attacker of type A5 (see [@attackermodel]) may be able to obtain DPoP proofs
that they can then replay.

This may also allow reuse of the DPoP proof with an altered request, as DPoP does
not sign the body of HTTP requests nor most headers. For example, for a payment request
the attacker might be able to specify a different amount or destination account.

Possible mitigations for this are:

1. Resource servers use short-lived DPoP nonces to reduce the time window where a request can be replayed.
2. Resource servers implement replay prevention using the `jti` header as explained in [@!RFC9449].
3. Replay of an altered request can be prevented by using signed resource requests as per FAPI Message Signing [@FAPIMessageSigning].
4. Consider MTLS sender-constraining instead of DPoP.

These mitigations may have potential complexity, performance or scalability trade-offs. Attacker type A5
represents a powerful attacker and mitigations may not be necessary for many ecosystems.

### JWKS URIs

This profile supports the use of `private_key_jwt` and in addition allows the use of
OpenID Connect. When these are used Clients and Authorization Servers need to verify
payloads with keys from another party. For Authorization Servers this profile strongly
recommends  the use of JWKS URI endpoints to distribute public keys. For Client's key
management this profile recommends either the use of JWKS URI endpoints or the use of
the `jwks` parameter in combination with [@!RFC7591] and [@!RFC7592].

The definition of the Authorization Server `jwks_uri` can be found in [@!RFC8414],
while the definition of the Client `jwks_uri` can be found in [@!RFC7591].

In addition, this profile

1. requires that `jwks_uri` endpoints shall be served over TLS;
1. recommends that JOSE headers for `x5u` and `jku` should not be used; and
1. recommends that the JWK set does not contain multiple keys with the same `kid`.

### Duplicate Key Identifiers

JWK sets should not contain multiple keys with the same `kid`. However, to increase
interoperability when there are multiple keys with the same `kid`,  the verifier shall
consider other JWK attributes, such as `kty`, `use`, `alg`, etc., when selecting the
verification key for the particular JWS message. For example, the following algorithm
could be used in selecting which key to use to verify a message signature:

1. find keys with a `kid` that matches the `kid` in the JOSE header;
2. if a single key is found, use that key;
3. if multiple keys are found, then the verifier should iterate through the keys until a key is found that has a matching `alg`, `use`, `kty`, or `crv` that corresponds to the message being verified.

### Injection of stolen access tokens

There are potential situations where the attacker may be able to inject stolen access
tokens into a client to bypass [@!RFC8705] or [@!RFC9449]
sender-constraining of the access token, as described in "Cuckoo's Token Attack" in
[@FAPI1SEC].

A pre-condition for this attack is that the attacker has control of an authorization
server that is trusted by the client to issue access tokens for the target resource
server. An attacker may obtain control of an authorization server by:

1. compromising the security of a different authorization server that the client trusts;
2. acting as an authorization server and establishing a trust relationship with a client using social engineering; or
3. compromising the client.

The attack may be easier if a centralized directory or other resource server discovery mechanism allows the attacker to
cause the client to send the stolen access token received from the attacker-controlled Authorization Server to an honest
Resource Server.

The pre-conditions for this attack do not apply to many ecosystems and require a powerful attacker. In situations
where the pre-conditions may be met, the possible mitigations include:

1. clients using different DPoP keys or MTLS certificates at each authorization server;
2. clients sending the issuer identifier the access token was obtained from to the resource server, and requiring
   resource servers to verify the issuer matches the authorization server that originally issued the token (though
   there is no standardized method for clients to send the issuer to the resource server);
3. reducing the time window for the attack by using short-lived access tokens alongside refresh tokens.

### Authorization Request Leaks lead to CSRF

An attacker of type A3 (see [@attackermodel]) can intercept an authorization request, log in at the
Authorization Server, receive an authorization code and redirect the honest user via a Cross-Site Request Forgery (CSRF) attack to
the honest client but with the attacker's authorization code. This results in the user accessing the
attacker's resources, thus breaking session integrity.

It is important to note that all practically used redirect-based flows are
susceptible to this attack, as redirection does not allow for a tight coupling
of the session between the user's browser and the client on the one side and the
session between the user's browser and the authorization server on the other
side.  This attack, however, requires a strong attacker who can read
authorization requests and perform a CSRF attack in a short time window.

Possible mitigations for this are:

1. Requiring the Authorization Server to only accept a `request_uri` once. This
   will prevent attacks where the attacker was able to read the authorization
   request, but not use the `request_uri` before the honest user does so.
2. Requiring the Client to only make one authorization code grant call for each
   authorization endpoint call. This will prevent attacks where the attacker was
   unable to send the authorization response before the honest user does so.
3. Reducing the lifetime of the authorization code - this will reduce the window
   in which the CSRF attack has to be performed.

An attacker that has the option to block a user's request completely can
circumvent the first and second defences. In practice, however, attackers can
often read an authorization request (e.g., from a log file or via some other
side-channel), but not block the request from being sent. If the victim's
internet connection is slow, this might increase the attacker's chances.

### Browser-Swapping Attacks

An attacker that has access to the authorization response sent through a
victim's browser can perform a browser-swapping attack as follows:

 1. The attacker starts a new flow using their own browser and some
    client. The client sends a pushed authorization request to the
    authorization server and receives a `request_uri` in the response.
    The client then redirects the attacker's browser to the
    authorization server.
 2. The attacker intercepts this redirection and forwards the URL to a
    victim. For example, the attacker can embed a link to this URL in a
    phishing website, an email, or a QR code.
 3. The victim may be tricked into believing that an
    authentication/authorization is legitimately required. The victim
    therefore authenticates at the authorization server and may grant
    the client access to their data.
 4. The attacker can now intercept the authorization response in the
    victim's browser and forward it to the client using their own browser.
 5. The client will recognize that the authorization response belongs to
    the same browser that initially started the transaction (the
    attacker's browser) and exchange the authorization code for an
    access token and/or obtain user information.
 6. Via the client, the attacker now has access to the user's resources
    or is logged in as the user.


With currently deployed technology, there is no way to completely
prevent this attack if the authorization response leaks to an attacker
in any redirect-based protocol. It is therefore important to keep the
authorization response confidential. The requirements in this security
profile are designed to achieve that, e.g., by disallowing open
redirectors and requiring that the `redirect_uri` is sent via an
authenticated and encrypted channel, the pushed authorization request,
ensuring that the `redirect_uri` cannot be manipulated by the attacker.

Implementers need to consider the confidentiality of the authorization
response critical when designing their systems, in particular when this
security profile is used in other contexts, e.g., mobile applications.

### Incomplete or incorrect implementations of the specifications {#incomplete-or-incorrect-implementations-of-the-specifications}

To achieve the full security and interoperability benefits, it is important that
the implementation of this specification and the underlying OpenID Connect and
OAuth specifications is both complete and correct.

The OpenID Foundation provides tools that can be used to confirm that an
implementation is correct:

https://openid.net/certification/

The OpenID Foundation maintains a list of certified implementations:

https://openid.net/developers/certified/

Deployments that use this specification should use certified implementations.


# Privacy considerations

There are many factors to be considered in terms of privacy when implementing
this specification. Since this specification is a profile of OAuth 2.0 and
OpenID Connect, the privacy considerations are not specific to this document and
generally apply to OAuth or OpenID Connect. Implementers are advised to perform
a thorough privacy impact assessment and manage identified risks appropriately.

**NOTE 1:** Implementers can consult documents like [@!ISO29100] and [@ISO29134] for this
purpose.

Privacy threats to OAuth and OpenID Connect implementations include the following:

  * **Inappropriate privacy notice**:  A privacy notice (e.g., provided at a
    `policy_url`) or by other means can be inappropriate or insufficient.
  * **Inadequate choice**:  Providing a consent screen without adequate choices
    does not form consent.
  * **Misuse of data**:  An authorization server, resource server or client can
    potentially use the data not according to the purpose that was agreed.
  * **Collection minimization violation**:  A client asking for more data than
    it absolutely needs to fulfill the purpose is violating the collection
    minimization principle.
  * **Unsolicited personal data from the resource server**:  Some bad resource
    server implementations may return more data than requested. If the data is
    personal data, then this would be a violation of privacy principles.
  * **Data minimization violation**:  Any process that is processing more data
    than it needs is violating the data minimization principle.
  * **Authorization servers tracking end-users**:  Authorization servers
    identifying what data is being provided to which client for which end-user.
  * **End-user tracking by clients**:  Two or more clients correlating access
    tokens or ID Tokens to track users.
  * **Client misidentification by end-users**:  End-user misunderstands who the
    client is due to a confusing representation of the client at the
    authorization server's authorization page.
  * **Insufficient understanding of the end-user granting access to data**: To
    enhance the trust of the ecosystem, best practice is for the authorization
    server to make clear what is included in the authorization request (for
    example, what data will be released to the client).
  * **Attacker observing personal data in authorization request/response**:  The authorization request or response might contain personal
    data. In some jurisdictions, even security parameters can be considered
    personal data. This profile aims to reduce the data sent in the
    authorization request and response to an absolute minimum, but nonetheless,
    an attacker might observe some data.
  * **Data leak from authorization server**:  The authorization server generally
    stores personal data. If it becomes compromised, this data can leak or be
    modified.
  * **Data leak from resource servers**:  Some resource servers store personal
    data. If a resource server becomes compromised, this data can leak or be
    modified.
  * **Data leak from clients**:  Some clients store personal data. If the client
    becomes compromised, this data can leak or be modified.


# Acknowledgements

This specification was developed by the OpenID FAPI Working Group.

We would like to thank Takahiko Kawasaki, Filip Skokan, Nat Sakimura, Stuart Low, Dima Postnikov, Torsten Lodderstedt, Travis Spencer, Brian Campbell, Ralph Bragg, Lukasz Jaromin, Pedram Hosseyni, Ralf Küsters and Tim Würtele for their valuable feedback and contributions that helped to evolve this specification.



{backmatter}

<reference anchor="attackermodel" target="https://openid.net/specs/fapi-2_0-attacker-model.html">
  <front>
    <title>FAPI 2.0 Attacker Model</title>
    <author initials="D." surname="Fett" fullname="Daniel Fett">
      <organization>Authlete</organization>
    </author>
   <date day="14" month="Nov" year="2022"/>
  </front>
</reference>

<reference anchor="FAPIMessageSigning" target="https://openid.bitbucket.io/fapi/fapi-2_0-message-signing.html">
  <front>
    <title>FAPI 2.0 Message Signing</title>
    <author initials="D." surname="Tonge" fullname="Dave Tonge">
      <organization>Moneyhub Financial Technology</organization>
    </author>
    <author initials="D." surname="Fett" fullname="Daniel Fett">
      <organization>Authlete</organization>
    </author>
   <date day="17" month="January" year="2024"/>
  </front>
</reference>

<reference anchor="GrantManagement" target="https://openid.net/specs/oauth-v2-grant-management-ID1.html">
  <front>
    <title>Grant Management for OAuth 2.0</title>
    <author initials="T." surname="Lodderstedt" fullname="Torsten Lodderstedt">
      <organization>yes.com</organization>
    </author>
    <author initials="S." surname="Low" fullname="Stuart Low">
      <organization>Biza.io</organization>
    </author>
    <author initials="D." surname="Postnikov" fullname="Dima Postnikov">
    </author>
   <date day="09" month="May" year="2023"/>
  </front>
</reference>

<reference anchor="FAPICIBA" target="https://openid.bitbucket.io/fapi/fapi-ciba.html">
  <front>
    <title>FAPI Client Initiated Backchannel Authentication Profile </title>
    <author initials="D." surname="Tonge" fullname="Dave Tonge">
      <organization>Moneyhub Financial Technology</organization>
    </author>
   <date day="17" month="January" year="2024"/>
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
<title>ISO/IEC Directives, Part 2 - Principles and rules for the structure and drafting of ISO and IEC documents</title>
    <author fullname="ISO/IEC">
      <organization>ISO/IEC</organization>
    </author>
</front>
</reference>


<reference anchor="ISO29100" target="https://standards.iso.org/ittf/PubliclyAvailableStandards/index.html#:~:text=IEC%2029100%3A2011-,EN,-%2D%20FR">
<front>
<title>ISO/IEC 29100 Information technology – Security techniques – Privacy framework</title>
    <author fullname="ISO/IEC">
      <organization></organization>
    </author>
</front>
</reference>

<reference anchor="ISO29134" target="https://www.iso.org/standard/86012.html">
<front>
<title>ISO/IEC 29134 Information technology – Security techniques – Guidelines for privacy impact assessment</title>
    <author fullname="ISO/IEC">
      <organization></organization>
    </author>
</front>
</reference>


<reference anchor="FAPI1SEC" target="https://arxiv.org/abs/1901.11520">
  <front>
    <title>An Extensive Formal Security Analysis of the OpenID Financial-grade API</title>
    <author initials="D." surname="Fett" fullname="Daniel Fett">
      <organization>yes.com AG</organization>
    </author>
    <author initials="P." surname="Hosseyni" fullname="Pedram Hosseyni">
      <organization>University of Stuttgart, Germany</organization>
    </author>
    <author initials="R." surname="Kuesters" fullname="Ralf Kuesters">
      <organization>University of Stuttgart, Germany</organization>
    </author>
    <date day="31" month="Jan" year="2019"/>
  </front>
</reference>


<reference anchor="BCP195" target="https://www.rfc-editor.org/info/bcp195">
  <front>
    <title>BCP195</title>
    <author>
      <organization>IETF</organization>
    </author>
  </front>
</reference>

# Notices

Copyright (c) 2022 The OpenID Foundation.

The OpenID Foundation (OIDF) grants to any Contributor, developer, implementer, or other interested party a non-exclusive, royalty free, worldwide copyright license to reproduce, prepare derivative works from, distribute, perform and display, this Implementers Draft or Final Specification solely for the purposes of (i) developing specifications, and (ii) implementing Implementers Drafts and Final Specifications based on such documents, provided that attribution be made to the OIDF as the source of the material, but that such attribution does not indicate an endorsement by the OIDF.

The technology described in this specification was made available from contributions from various sources, including members of the OpenID Foundation and others. Although the OpenID Foundation has taken steps to help ensure that the technology is available for distribution, it takes no position regarding the validity or scope of any intellectual property or other rights that might be claimed to pertain to the implementation or use of the technology described in this specification or the extent to which any license under such rights might or might not be available; neither does it represent that it has made any independent effort to identify any such rights. The OpenID Foundation and the contributors to this specification make no (and hereby expressly disclaim any) warranties (express, implied, or otherwise), including implied warranties of merchantability, non-infringement, fitness for a particular purpose, or title, related to this specification, and the entire risk as to implementing this specification is assumed by the implementer. The OpenID Intellectual Property Rights policy requires contributors to offer a patent promise not to assert certain patent claims against other contributors and against implementers. The OpenID Foundation invites any interested party to bring to its attention any copyrights, patents, patent applications, or other proprietary rights that may cover technology that may be required to practice this specification.
