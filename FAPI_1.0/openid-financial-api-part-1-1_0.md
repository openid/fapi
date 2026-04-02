---
title: FAPI security profile 1.0 - Part 1&colon; Baseline - draft 11 incorporating errata set 1
date: 2026-03-27
author: 
- name: Nat Sakimura
  organization: Nat.Consulting
  email: nat@nat.consulting
  uri: http://nat.sakimura.org/
- name: John Bradley
  organization: Yubico
  email: ve7jtb@ve7jtb.com
  uri: http://www.thread-safe.com/
- name: Edmund Jay
  organization: Illumila
  email: ejay@mgi1.com
  uri: http://illumila.la/
description: 
  Profile of OAuth with medium security options.    
keywords:
- FAPI
- Baseline security
toc: true
toc-title: Table of contents
draft: true
implementers-draft: false
final: false
ver: 11
seriesInfo:
  name: Internet-Draft
  value: openid-financial-api-part-1-1_0-11
  status: draft
WG: FAPI
...


FAPI 1.0 consists of the following parts:

* FAPI Security Profile 1.0 - Part 1: Baseline
* [FAPI Security Profile 1.0 - Part 2: Advanced][Part2]

These parts are intended to be used with [RFC 6749], [RFC 6750], [RFC 7636], and [OIDC].

# Introduction {-}

FAPI is a highly secured OAuth profile that aims to provide specific implementation guidelines for security and interoperability. The FAPI security profile can be applied to APIs in any market area that requires a higher level of security than provided by standard [OAuth][RFC 6749] or [OpenID Connect][OIDC]. Among other security enhancements, this specification provides a secure alternative to screen scraping. Screen scraping accesses user's data and functions by impresonating a user through password sharing. This brittle, inefficient, and insecure practice creates security vulnerabilities which require financial institutions to allow what appears to be an automated attack against their applications.

This document is Part 1 of FAPI Security Profile 1.0. It specifies a baseline security profile of OAuth that is suitable for protecting APIs with a moderate inherent risk. Importantly, this profile does not provide non-repudiation (signing of authorization requests and responses) and sender-constrained access tokens. If such features or a higher level of security is desired, the use of [FAPI Security Profile 1.0 - Part 2: Advanced][Part2] is recommended.

Although it is possible to code an OpenID provider and relying party from first principles using this specification, the main audience for this specification is parties who already have a certified implementation of OpenID Connect and want to achieve a higher level of security. Implementers are encouraged to understand the security considerations contained in Section 7.6 before embarking on a 'from scratch' implementation.

# Notational Conventions

The keywords "shall", "shall not", "should", "should not", "may", and "can" in this document are to be interpreted as described in [ISO Directive Part 2][ISODIR2]. These keywords are not used as dictionary terms such that any occurrence of them shall be interpreted as keywords and are not to be interpreted with their natural language meanings.


# 1. Scope

This document specifies the method for an application to:

* obtain OAuth tokens in a moderately secure manner for access to protected data;
* use OpenID Connect (OIDC) to identify the customer (user); and 
* use tokens to access REST APIs in a moderately secure manner.

# 2. Normative references
The following documents are referred to in the text in such a way that some or all of their content constitutes requirements of this document. For dated references, only the edition cited applies. For undated references, the latest edition of the referenced document (including any amendments) applies.

[RFC 4122], A Universally Unique IDentifier (UUID) URN Namespace

[RFC 4122]: https://tools.ietf.org/html/rfc4122

[RFC 6749], The OAuth 2.0 Authorization Framework

[RFC 6749]: https://tools.ietf.org/html/rfc6749

[RFC 7636], Proof Key for Code Exchange by OAuth Public Clients

[RFC 7636]: https://tools.ietf.org/html/rfc7636

[RFC 6125], Representation and Verification of Domain-Based Application Service Identity within Internet Public Key Infrastructure Using X.509 (PKIX) Certificates in the Context of Transport Layer Security (TLS)

[RFC 6125]: https://tools.ietf.org/html/rfc6125

[BCP 212], OAuth 2.0 for Native Apps

[BCP 212]: https://tools.ietf.org/html/bcp212

[BCP 195], Recommendations for Secure Use of Transport Layer Security (TLS) and Datagram Transport Layer Security (DTLS)

[BCP 195]: https://tools.ietf.org/html/bcp195

[IANA TLSP], Transport Layer Security (TLS) Parameters

[IANA TLSP]: https://www.iana.org/assignments/tls-parameters/tls-parameters.xhtml

[OIDC], OpenID Connect Core 1.0

[OIDC]: https://openid.net/specs/openid-connect-core-1_0.html

[RFC 8705], OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens

[RFC 8705]: https://tools.ietf.org/html/rfc8705

[OIDD], OpenID Connect Discovery 1.0

[OIDD]: https://openid.net/specs/openid-connect-discovery-1_0.html

[RFC 7231], Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content

[RFC 7231]: https://tools.ietf.org/html/rfc7231

# 3. Terms and definitions
For the purpose of this document, the terms defined in [RFC 6749], [RFC 6750], [RFC 7636], [OIDC] apply.


# 4. Abbreviated terms
--------- --- ----------------------------------
**API**       application programming interface
**CAA**       certificate authority authorization
**CORS**      cross-origin resource sharing
**CSRF**      cross site request forgery
**DNSSEC**    domain name system security extensions
**FAPI**      FAPI
**HTTP**      hyper text transfer protocol
**IP**        internet protocol
**JARM**      JWT secured authorization response mode
**JSON**      javaScript object notation
**JWT**       JSON web token
**OIDF**      OpenID foundation
**RP**        relying party
**RSA**       Rivest–Shamir–Adleman
**REST**      representational state transfer
**TLS**       transport layer security
**URI**       uniform resource identifier
**UTF**       unicode transformation format
**UUID**      universally unique identifier
--------- --- ----------------------------------

# 5. Baseline security profile

## 5.1 Introduction

The OIDF FAPI security profile specifies security requirements for API resources protected by the OAuth 2.0 Authorization Framework that consists of [RFC 6749], [RFC 6750], [RFC 7636], and other specifications.

FAPI Security Profile 1.0 - Part 1: Baseline and [Part 2: Advanced][Part2] specify different levels of security. The characteristics required of the tokens are different and the methods to obtain tokens are explained separately. This document specifies the baseline security provisions.

## 5.2 Baseline security provisions

### 5.2.1 Introduction

Some APIs, such as ones that provide potentially sensitive information, require a greater level of protection than basic [RFC 6749] requires. FAPI provides such greater protection.

As a profile of the OAuth 2.0 Authorization Framework, this document mandates the following to the baseline profile of the FAPI Security Profile 1.0.

### 5.2.2 Authorization server

#### 5.2.2.0 Authorization server provisions

The authorization server

1. shall support confidential clients;
1. should support public clients; 
1. shall provide a client secret that adheres to the requirements in Section 16.19 of [OIDC] if a symmetric key is used;
1. shall authenticate the confidential client using one of the following methods:
    1. Mutual TLS for OAuth client authentication as specified in Section 2 of [RFC 8705], or
    2. `client_secret_jwt` or `private_key_jwt` as specified in Section 9 of [OIDC];
1. shall require and use the key length permitted by [BCP 195];
1. shall not use algorithms deprecated in [IANA TLSP];
1. shall require [RFC 7636] with `S256` as the code challenge method;
1. shall require redirect URIs to be pre-registered;
1. shall require the `redirect_uri` in the authorization request;
1. shall require the value of `redirect_uri` to exactly match one of the pre-registered redirect URIs;
1. shall require user authentication to an appropriate level of assurance for the operations the client will be authorized to perform on behalf of the user;
1. shall require explicit approval by the user to authorize the requested scope if it has not been previously authorized;
1. shall reject an authorization code (Section 1.3.1 of [RFC 6749]) if it has been previously used;
1. shall return token responses that conform to Section 4.1.4 of [RFC 6749]; 
1. shall return the list of granted scopes with the issued access token if the request was passed in the front channel and was not integrity protected;
1. shall provide non-guessable access tokens, authorization codes, and refresh token 
(where applicable), with sufficient entropy such that the probability of an attacker guessing 
the generated token is computationally infeasible as per [RFC 6749] Section 10.10;
1. should clearly identify the details of the grant to the user during authorization as in 16.18 of [OIDC]; 
1. should provide a mechanism for the end-user to revoke access tokens and refresh tokens granted to a client as in 16.18 of [OIDC];
1. shall return an `invalid_client` error as defined in 5.2 of [RFC 6749] when mis-matched client identifiers were provided through the client authentication methods that permits sending the client identifier in more than one way;
1. shall require redirect URIs to use the https scheme;
1. should issue access tokens with a lifetime of under 10 minutes unless the tokens are sender-constrained; and
1. shall support [OIDD], may support [RFC 8414] and shall not distribute discovery metadata (such as the authorization endpoint) by any other means.
1. shall require the `response_type` values `code` or `code id_token`

    **NOTE**: The use of refresh tokens instead of long-lived access tokens for both 
    public and confidential clients is recommended.

    **NOTE**: The FAPI Security Profile 1.0 authorization server may limit the scopes for the purpose of not implementing certain APIs.

    **NOTE**: Clients are expected to treat access tokens as opaque strings and replay them as is. Authorization servers can issue unstructured or structured access tokens (for example, a signed JWT).

    **NOTE**: The requirement to return the list of granted scopes allows clients to detect when the authorization request was modified to include different scopes. Servers must still return the granted scopes per section 5.1. of [RFC 6749] if they are different from those requested.

#### 5.2.2.1 Returning authenticated user's identifier

Further, if it is desired to provide the authenticated user's identifier to the client in the token response, the authorization server:

1. shall support the authentication request as in Section 3.1.2.1 of [OIDC];
1. shall perform the authentication request verification as in Section 3.1.2.2 of [OIDC];
1. shall authenticate the user as in Section 3.1.2.2 and 3.1.2.3 of [OIDC];
1. shall provide the authentication response as in Section 3.1.2.4 and 3.1.2.5 of [OIDC] depending on the outcome of the authentication;
1. shall perform the token request verification as in Section 3.1.3.2 of [OIDC]; and
1. shall issue an ID Token in the token response when `openid` was included in the requested `scope`
   as in Section 3.1.3.3 of [OIDC] with its `sub` value corresponding to the authenticated user
   and optional `acr` value in ID Token.

#### 5.2.2.2 Client requesting openid scope

If the client requests the openid scope, the authorization server

1. shall require the `nonce` parameter defined in Section 3.1.2.1 of [OIDC] in the authentication request.

#### 5.2.2.3 Clients not requesting openid scope

If the client does not request the openid scope, the authorization server

1. shall require the `state` parameter defined in Section 4.1.1 of [RFC 6749].

### 5.2.3 Public client

A public client

1. shall support [RFC 7636];
2. shall use `S256` as the code challenge method for the [RFC 7636];
3. shall use separate and distinct redirect URI for each authorization server that it talks to;
4. shall store the redirect URI value in the resource owner's user-agents (such as browser) session and compare it with the redirect URI that the authorization response was received at, where, if the URIs do not match, the client shall terminate the process with error;
5. (withdrawn); and
6. shall implement an effective CSRF protection.

Further, if it is desired to obtain a persistent identifier of the authenticated user, then the public client

7. shall include `openid` in the `scope` value; and
8. shall include the `nonce` parameter defined in Section 3.1.2.1 of [OIDC] in the authentication request.

If `openid` is not in the `scope` value, then the public client

9. shall include the `state` parameter defined in Section 4.1.1 of [RFC 6749].

Further, a client 

10. shall verify that the `scope` received in the token response is either an exact match,
or contains a subset of the `scope` sent in the authorization request if the request was passed in the front channel and was not integrity protected; and
11. shall only use authorization server metadata obtained from the metadata document published by the authorization server at its well known endpoint as defined in [OIDD] or [RFC 8414].

    **NOTE**: Adherence to [RFC 7636] means that the token request includes `code_verifier` parameter in the request.


### 5.2.4 Confidential client

In addition to the provisions for a public client, a confidential client

1. shall support the following methods to authenticate against the token endpoint:
    1. Mutual TLS for OAuth client authentication as specified in Section 2 of [RFC 8705], and
    2. `client_secret_jwt` or `private_key_jwt` as specified in Section 9 of [OIDC];
1. shall require and use the key length permitted by [BCP 195]; 
1. shall not use algorithms deprecated in [IANA TLSP]; and
1. shall verify that its client secret has a minimum of 128 bits if using symmetric key cryptography.


# 6. Accessing protected resources

## 6.1 Introduction

The FAPI endpoints are OAuth 2.0 protected resource endpoints that return protected information for the resource owner associated with the submitted access token.

## 6.2 Baseline access provisions

### 6.2.1 Protected resources provisions

The resource server with the FAPI endpoints

1. shall support the use of the HTTP GET method as in Section 4.3.1 of [RFC 7231];
1. shall accept access tokens in the HTTP header as in Section 2.1 of OAuth 2.0 Bearer Token Usage [RFC 6750];
1. shall not accept access tokens in the query parameters stated in Section 2.3 of OAuth 2.0 Bearer Token Usage [RFC 6750];
1. shall verify that the access token is neither expired nor revoked;
1. shall verify that the scope associated with the access token authorizes access to the resource it is representing;
1. shall identify the associated entity to the access token;
1. shall only return the resource identified by the combination of the entity implicit in the access and the granted scope and otherwise return errors as in Section 3.1 of [RFC 6750];
1. shall encode the response in UTF-8 if applicable; 
1. shall send the `Content-type` HTTP header `Content-Type: application/json` if applicable;
1. shall send the server date in HTTP Date header as in Section 7.1.1.2 of [RFC 7231];
1. shall set the response header `x-fapi-interaction-id` to the value received from the corresponding FAPI client request header or to an [RFC 4122] UUID value if the request header was not provided to track the interaction, e.g., `x-fapi-interaction-id: c770aef3-6784-41f7-8e0e-ff5f97bddb3a`;
1. shall log the value of `x-fapi-interaction-id` in the log entry; and
1. shall not reject requests with a `x-fapi-customer-ip-address` header containing a
valid IPv4 or IPv6 address.

    **NOTE**: While this document does not specify the exact method to obtain the entity associated with the
    access token and the granted scope, the protected resource can use OAuth Token Introspection [RFC 7662].

Further, the resource server

1. should support the use of Cross Origin Resource Sharing (CORS) [CORS] and or other methods as appropriate to enable JavaScript clients to access the endpoint if it decides to provide access to JavaScript clients.

    **NOTE**: Providing access to JavaScript clients has other security implications. Before supporting those clients [RFC 6819] should be consulted.

### 6.2.2 Client provisions

The client supporting this document

1. shall send access tokens in the HTTP header as in Section 2.1 of OAuth 2.0 Bearer Token Usage [RFC 6750]; and 
1. (withdrawn);

Further, the client

1. may send the last time the customer logged into the client in the `x-fapi-auth-date` header where the value is supplied as an HTTP-date as in Section 7.1.1.1 of [RFC 7231], e.g., `x-fapi-auth-date: Tue, 11 Sep 2012 19:43:31 GMT`;
1. may send the customer’s IP address if this data is available in the `x-fapi-customer-ip-address` header, e.g., `x-fapi-customer-ip-address: 2001:DB8::1893:25c8:1946` or  `x-fapi-customer-ip-address: 198.51.100.119`; and
1. may send the `x-fapi-interaction-id` request header, in which case the value shall be an 
[RFC 4122] UUID to the server to help correlate log entries between client and server, 
e.g., `x-fapi-interaction-id: c770aef3-6784-41f7-8e0e-ff5f97bddb3a`.


# 7. Security considerations

## 7.1 TLS and DNSSEC considerations

As confidential information is being exchanged, all interactions shall be encrypted with TLS (HTTPS).

The recommendations for Secure Use of Transport Layer Security in [BCP 195] shall be followed, with the following additional requirements:

1. TLS version 1.2 or later shall be used for all communications.
1. A TLS server certificate check shall be performed, as per [RFC 6125].

Endpoints for the use by web browsers should use mechanisms to ensure that connections cannot be downgraded using TLS stripping attacks. A preloaded HTTP Strict Transport Security policy (see [PRELOAD] and [RFC 6797]) can be used for this purpose. Some top-level domains, like `.bank` and `.insurance`, have set such a policy and therefore protect all second-level domains below them.

For a comprehensive protection against network attackers, all
endpoints should additionally use DNSSEC to protect against DNS
spoofing attacks that can lead to the issuance of rogue
domain-validated TLS certificates.

**NOTE**: Even if an endpoint uses only
organization validated (OV) or extended validation (EV) TLS
certificates, rogue domain-validated certificates can be used to
impersonate the endpoints and conduct man-in-the-middle attacks.
CAA records [RFC 8659] can help to mitigate this risk.

## 7.2 Message source authentication failure

Authorization request and response are not authenticated. 
For higher risk scenarios, they should be authenticated.
See [FAPI Security Profile 1.0 - Part 2: Advanced][Part2], which uses request objects, and ID Token or [JARM] to achieve the message source authentication. 

## 7.3 Message integrity protection failure

The authorization request does not have message integrity protection and hence
request tampering and parameter injection are possible.
Where such protection is desired, [FAPI Security Profile 1.0 - Part 2: Advanced][Part2] should be used.

The response is integrity protected when the ID Token is returned
from the authorization endpoint. 

## 7.4 Message containment failure

### 7.4.1 Authorization request and response

In this document, the authorization request is not encrypted. 
Thus, it is possible to leak the information contained 
if the web browser is compromised. If authorization request 
encryption is desired, the use of 
[FAPI Security Profile 1.0 - Part 2: Advanced][Part2] is recommended.

The leakage of information from the ID token can be mitigated by encrypting the ID token. 
If the leakage of any other information in the authorization response is of concern 
then consider using [JARM] with encryption.

It is possible to leak the information through the logs 
if the parameters were recorded in the logs and 
the access to the logs are compromised. 
Strict access control to the logs in such cases should be 
enforced. 

### 7.4.2 Token request and response

It is possible to leak information through the logs 
if the parameters were recorded in the logs and 
the access to the logs are compromised. 
Strict access control to the logs in such cases should be 
enforced. 

### 7.4.3 Resource request and response

Care should be taken so that the sensitive data will not be leaked 
through the referrer. 

If the access token is a bearer token, it is possible to 
exercise the stolen token. Since the access token can be 
used against multiple URIs, the risk of leaking is
much larger than the refresh token, which is used only 
against the token endpoint. Thus, the lifetime of 
the access token should be much shorter than that of 
the refresh token. Refer to Section 16.18 of [OIDC] for 
more discussion on the lifetimes of access tokens and 
refresh tokens. 

## 7.5 Native apps

When native apps are used as either public clients, dynamically registered confidential clients or user-agents receiving the authorization response for a server based confidential client, the recommendations for OAuth 2.0 for Native Apps in [BCP 212] shall be followed, with the following additional requirements:

When registering redirect URIs, authorization servers

1. shall not support "private-use URI scheme redirection"; and
1. shall not support "loopback interface redirection".

These requirements mean that FAPI Security Profile 1.0 compliant implementations can only
support native apps through the use of "claimed HTTPS scheme URI redirection".

**NOTE**: Nothing in this document seeks to disallow fixed urls in the
form https://localhost:port-number/callback, as these are particularly
useful in non-production systems or in clients used in development, to
facilitate faster and easier development.

## 7.6 Incomplete or incorrect implementations of the specifications

To achieve the full security benefits, it is important the implementation of this specification, and the underlying OpenID Connect and OAuth specifications, are both complete and correct.

The OpenID Foundation provides tools that can be used to confirm that an implementation is correct:

[https://openid.net/certification/](https://openid.net/certification/)

The OpenID Foundation maintains a list of certified implementations:

[https://openid.net/developers/certified/](https://openid.net/developers/certified/)

Deployments that use this specification should use a certified implementation.

## 7.7 Discovery & multiple brands

Organizations who need to support multiple "brands" with individual authorization endpoints 
from a single authorization server deployment shall use a separate `issuer` per brand.
This can be achieved either at the domain level (e.g. `https://brand-a.auth.example.com` 
and  `https://brand-b.auth.example.com`) or with different paths (e.g. `https://auth.example.com/brand-a` and `https://auth.example.com/brand-b`)

As stated in 5.2.2.0-22 clients shall only use metadata values obtained via metadata documents
as defined in [OIDD]. Communicating metadata through other means (e.g. via email) opens 
up a social engineering attack vector.

Note that the requirement to use [OIDD] is not a requirement to support dynamic client 
registration. 

# 8. Privacy considerations

There are many factors to be considered in terms of privacy 
when implementing this document. However, since this document 
is a profile of OAuth and OpenID Connect, all of them 
are generic and apply to OAuth or OpenID Connect and 
are not specific to this document. Implementers are advised to 
perform a thorough privacy impact assessment and manage identified risks appropriately.

**NOTE**: Implementers can consult documents like
[ISO/IEC 29100] and [ISO/IEC 29134] for this purpose. 

Privacy threats to OAuth and OpenID Connect implementations include the following: 

* (Inappropriate privacy notice) A privacy notice provided at a `policy_url` or by other means can be inappropriate. 
* (Inadequate choice) Providing a consent screen without adequate choices does not form consent. 
* (Misuse of data) An authorization server, resource server or client can potentially use the data not according to the purpose that was agreed. 
* (Collection minimization violation) A client asking for more data than it absolutely needs to fulfil the purpose is violating the collection minimization principle. 
* (Unsolicited personal data from the resource) Some bad resource server implementations may return more data than was requested. If the data is personal data, then this would be a  violation of privacy principles. 
* (Data minimization violation) Any process that is processing more data than it needs is violating the data minimization principle. 
* (RP tracking by authorization server/OpenID provider) Authorization server/OpenID provider identifying what data is being provided to which client/RP. 
* (User tracking by RPs) Two or more RPs correlating access tokens or ID Tokens to track users. 
* (RP misidentification by user at authorization server) User misunderstands who the RP is due to a confusing representation of the RP at 
the authorization server's authorization page. 
* (Mismatch between user’s understanding or what RP is displaying to a user and the actual authorization request) To enhance 
the trust of the ecosystem, best practice is for the authorization server to make clear what is included in the authorization request (for example, 
what data will be released to the RP).
* (Attacker observing personal data in authorization request) Authorization request might contain personal data. This can be observed by an attacker. 
* (Attacker observing personal data in authorization endpoint response) In some frameworks, even state is deemed personal data. 
  This can be observed by an attacker through various means. 
* (Data leak from authorization server) Authorization server stores personal data. If authorization server is compromised, these data can leak or be modified. 
* (Data leak from resource) Some resource servers store personal data. If a resource server is compromised, these data can leak or be modified. 
* (Data leak from clients) Some clients store personal data. If the client is compromised, these data can leak or be modified. 

These threats can be mitigated by choosing appropriate options in OAuth or OpenID Connect, or by introducing some operational rules. 
For example, "attacker observing personal data in authorization request" can be mitigated by either using authorization request by reference 
using `request_uri` or by encrypting the request object. 
Similarly, "attacker observing personal data in authorization endpoint response" can be mitigated by encrypting the ID Token or [JARM] response. 

# Annex A (Informative) Acknowledgement {-}

The following people contributed to this document:

* Nat Sakimura (NAT Consulting) -- Chair, Editor
* Anoop Saxena (Intuit) -- Co-chair, FS-ISAC Liaison
* Anthony Nadalin (Microsoft) -- Co-chair, SC 27 Liaison
* Edmund Jay (Illumila) -- Co-editor
* Dave Tonge (Moneyhub) -- Co-chair, UK Implementation Entity Liaison
* Paul A. Grassi (NIST) -- X9 Liaison
* Joseph Heenan (Authlete)
* Sascha H. Preibisch (CA) 
* Henrik Biering (Peercraft)
* Anton Taborszky (Deutsche Telecom) 
* John Bradley (Yubico)
* Tom Jones (Independent)
* Axel Nennker (Deutsche Telekom)
* Daniel Fett (yes.com)
* Torsten Lodderstedt (yes.com)
* Ralph Bragg (Raidiam)
* Brian Campbell (Ping Identity)
* Dima Postnikov (Independent)
* Stuart Low (Biza.io)
* Takahiko Kawasaki (Authlete)
* Vladimir Dzhuvinov (Connect2Id)
* Chris Michael (Open Banking)
* Freddi Gyara (Open Banking)
* Rob Otto (Ping Identity)
* Francis Pouatcha (adorsys)
* Kosuke Koiwai (KDDI)
* Bjorn Hjelm (Verizon)
* Lukasz Jaromin (Cloudentity)
* James Manger

# Appendix B (Informative) Changes {-}

To be removed at the publication time. 

* 2026-02-27
    * Fixing the editorial issues pointed out by ISO. 
* 2023-06-25
    * Reformatting to the pandoc markdown
    * #600 - Changed Financial-grade API to FAPI
    * Changed the title to incorporate "errata"
    * #494 - 5.2.3-10 clarifies requirement for clients to verify the token endpoint's scope response if using 
      non-integrity protected front-channel requests
    * #428 - Recommends usage of [Part2] if authorization request encryption is desired and [JARM] for 
      authorization response information leakage mitigation
    * #405 - Use https for document references
    * #601 - Removed subclause 8.1 title 
    * #409 - Rename [MTLS] as [RFC 8705]
    * #458 - Clarifies that authorization server require response_type = code or code, id_token


# Bibliography {-}

* [Part2] FAPI Security Profile 1.0 - Part 2: Advanced

[Part2]: https://openid.net/specs/openid-financial-api-part-2-1_0.html

* [ISODIR2] - ISO/IEC Directives, Part 2 - Principles and rules for the structure and drafting of ISO and IEC documents

[ISODIR2]: https://www.iso.org/sites/directives/current/part2/index.xhtml

* [ISO/IEC 29100] ISO/IEC 29100 Information technology — Security techniques — Privacy framework

[ISO/IEC 29100]: https://www.iso.org/standard/85938.html

* [ISO/IEC 29134] ISO/IEC 29134 Information technology — Security techniques — Guidelines for privacy impact assessment

[ISO/IEC 29134]: https://www.iso.org/standard/86012.html

* [RFC 6750] The OAuth 2.0 Authorization Framework: Bearer Token Usage

[RFC 6750]: https://tools.ietf.org/html/rfc6750

* [RFC 6797] HTTP Strict Transport Security (HSTS)

[RFC 6797]: https://tools.ietf.org/html/rfc6797

* [RFC 7662] OAuth 2.0 Token Introspection

[RFC 7662]: https://tools.ietf.org/html/rfc7662

* [RFC 6819] OAuth 2.0 Threat Model and Security Considerations

[RFC 6819]: https://tools.ietf.org/html/rfc6819

* [RFC 8414] OAuth 2.0 Authorization Server Metadata

[RFC 8414]: https://tools.ietf.org/html/rfc8414 

* [RFC 8659] DNS Certification Authority Authorization (CAA) Resource Record

[RFC 8659]: https://tools.ietf.org/html/rfc8659

* [PRELOAD] HSTS Preload List Submission

[PRELOAD]: https://hstspreload.org/

* [JARM] JWT Secured Authorization Response Mode for OAuth 2.0 (JARM)

[JARM]: https://openid.net/specs/oauth-v2-jarm.html

* [CORS] Cross-Origin Resource Sharing

[CORS]: https://www.w3.org/TR/2020/SPSD-cors-20200602/



