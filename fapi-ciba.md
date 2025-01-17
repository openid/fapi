%%%
title = "FAPI Client Initiated Backchannel Authentication Profile - draft"
abbrev = "fapi-ciba"
ipr = "none"
workgroup = "fapi"
keyword = ["security", "openid", "ciba"]

[seriesInfo]
name = "Internet-Draft"
value = "fapi-ciba-03"
status = "standard"

[[author]]
initials="D."
surname="Tonge"
fullname="Dave Tonge"
organization="Moneyhub Financial Technology"
[author.address]
email = "dave@tonge.org"

%%%

.# Foreword

The OpenID Foundation (OIDF) promotes, protects and nurtures the OpenID community and technologies. As a non-profit international standardizing body, it is comprised by over 160 participating entities (workgroup participant). The work of preparing implementer drafts and final international standards is carried out through OIDF workgroups in accordance with the OpenID Process. Participants interested in a subject for which a workgroup has been established have the right to be represented in that workgroup. International organizations, governmental and non-governmental, in liaison with OIDF, also take part in the work. OIDF collaborates closely with other standardizing bodies in the related fields.

Final drafts adopted by the Workgroup through consensus are circulated publicly for the public review for 60 days and for the OIDF members for voting. Publication as an OIDF Standard requires approval by at least 50% of the members casting a vote. There is a possibility that some of the elements of this document may be subject to patent rights. OIDF shall not be held responsible for identifying any or all such patent rights.

.# Introduction

The FAPI Working Group produces security profiles based on the OAuth 2.0 Authorization Framework and related specifications suitable for protecting APIs in high-value scenarios.

This document is a profile of the OpenID Connect Client Initiated Backchannel Authentication Flow [@!CIBA]. The CIBA spec allows a client that gains knowledge of an identifier for the user to obtain tokens from the authorization server. The user consent is given at the user's authentication device mediated by the authorization server. This document profiles the CIBA specification to bring it in line with FAPI Security Profiles and provides security recommendations for its use with APIs that require high levels of security.

This profile may be used with either:

1. FAPI API Security Profile 1.0 - Parts 1 and 2 or
2. FAPI 2.0 Security Profile

.# Warning

This document is not an OIDF International Standard. It is distributed for
review and comment. It is subject to change without notice and may not be
referred to as an International Standard.

Recipients of this draft are invited to submit, with their comments,
notification of any relevant patent rights of which they are aware and to
provide supporting documentation.

.# Notational conventions

The keywords "shall", "shall not", "should", "should not", "may", and "can" in
this document are to be interpreted as described in ISO Directive Part 2
[@ISODIR2]. These keywords are not used as dictionary terms such that any
occurrence of them shall be interpreted as keywords and are not to be
interpreted with their natural language meanings.

{mainmatter}

# Scope

This document specifies the method for an application to:

- obtain OAuth tokens via a backchannel authentication flow in an appropriately secure manner for high-value data access and other similar situations where the risk is higher;
- use tokens to interact with protected data via REST endpoints.

# Terms and definitions

For the purpose of this standard, the terms defined in RFC6749, RFC6750, RFC7636, OpenID Connect Core and OpenID Connect Client Initiated Backchannel Authentication Core apply.

# Symbols and abbreviated terms

**API** – Application Programming Interface

**CCTV** – Closed Circuit Television

**CIBA** – Client Initiated Backchannel Authentication

**HTTP** – Hyper Text Transfer Protocol

**HTTPS** – Hypertext Transfer Protocol Secure

**JSON** – JavaScript Object Notation

**JWE** – JSON Web Encryption

**JWS** – JSON Web Signature

**JWT** – JSON Web Token

**OIDF** – OpenID Foundation

**QR** – Quick Response

**POS** – Point-of-Sale

**REST** – Representational State Transfer

**TLS** – Transport Layer Security

# Client initiated backchannel authentication security profile

The standard OAuth method for the client to send the resource owner to the authorization server is to use an HTTP redirect. FAPI specification support this interaction model and are suitable for use cases where the resource owner is interacting with the client on a device they control that has a web browser. There are however many use-cases for initiating payments where the resource owner is not interacting with the client in such a manner. For example, the resource owner may want to authorize a payment at a "point of sale" terminal at a shop or fuel station.

The Client Initiated Backchannel Authentication Flow [@!CIBA] specifies an alternate method of users granting access to their resources whereby the flow is started from a consumption device, but authorized on an authentication device.

The following sections specify a profile of CIBA that is suited for high-value transactions and sensitive (personal and other) data.

## Client initiated backchannel authentication security provisions

When this profile is used with the FAPI 1.0 specifications then it should be read in conjunction with OpenID Connect Client Initiated Backchannel Authentication Core [@!CIBA] and with parts 1 [@!FAPI1.1] and 2 [@!FAPI1.2] of the FAPI 1.0 Specifications.

When this profile is used with the FAPI 2.0 specifications then it should be read in conjunction with OpenID Connect Client Initiated Backchannel Authentication Core [@!CIBA] and the FAPI 2.0 Security Profile [@!FAPI2].

### Authorization server

When this profile is used with the FAPI 1.0 specifications, the authorization server
shall support the provisions specified in clause 5.2.2 of [@!FAPI1.1] and [@!FAPI1.2].

When this profile is used with the FAPI 2.0 specifications, the authorization server
shall support the general requirements for authorization servers listed in clause
5.3.1.1 of [@!FAPI2].

In addition the authorization server

1. shall only support confidential clients for client initiated backchannel authentication flows;
1. shall ensure unique authorization context exists in the authentication request or require a binding_message in the authentication request;
1. shall not support CIBA push mode;
1. shall support CIBA poll mode;
1. may support CIBA ping mode;
1. shall, if it supports the acr claim and the client has requested acr, return an 'acr' claim in the resulting ID token;
1. should not use the login_hint or login_hint_token to convey "intent ids" or any other authorization metadata; and
1. may require clients to provide a `request_context` claim as defined in Section 4.3 of this profile.

When this profile is used with the FAPI 1.0 specifications, the authorization server

1. shall support unsigned and signed backchannel authentication endpoint requests as described in [@!CIBA] 7.1.1; and
1. shall require the signed authentication request to contain `nbf` and `exp` claims that limit the lifetime of the request to no more than 60 minutes.

**NOTE:** As per [@!CIBA], `login_hint`, `login_hint_token` and `id_token_hint` are used only to determine who the user is. In scenarios where complex authorization parameters need to be conveyed from the client to the authorization server, implementers should consider using OAuth 2.0 Rich Authorization Requests [@!RAR]. The use of parameterized scope values or the use of an additional request parameter are both supported by this specification.

**NOTE:** The binding message is required to protect the user by binding the session on the consumption device with the session on the authentication device. An example use case is when a user is paying at POS terminal. The user will enter their user identifier to start the [@!CIBA] flow, the terminal will then display a code, the user will receive a notification on their phone (the authentication device) to ask them to authenticate and authorize the transaction, as part of the authorization process the user will be shown a code and will be asked to check that it is the same as the one shown on the terminal.

**NOTE:** The FAPI CIBA profile only supports CIBA ping and poll modes, therefore it is only possible to retrieve access tokens and optionally refresh tokens from the token endpoint.

**NOTE:** While the format of the `login_hint` and `login_hint_token` parameters are not defined by [@!CIBA] or this profile, implementers may wish to consider https://tools.ietf.org/html/draft-ietf-secevent-subject-identifiers for a standards based method of communicating user identifiers.

**NOTE:** As per [@!CIBA], if the Client authenticates using a client assertion as described in Section 4.2 of [@!RFC7521], the authorization server MUST verify that it is the sole audience of the assertion, with the issuer identifier [RFC8414] of the authorization server as its sole value.

### Confidential client

When this profile is used with the FAPI 1.0 specifications, a confidential client shall
support the provisions specified in clause 5.2.4 of [@!FAPI1.1] and [@!FAPI1.2].

When this profile is used with the FAPI 2.0 specifications, a confidential client shall
support the general requirements for clients listed in clause 5.3.2.1 of [@!FAPI2].

In addition, the confidential client

1. shall ensure sufficient authorization context exists in authorization request or shall include a binding_message in the authentication request; and

When this profile is used with the FAPI 1.0 specifications, the confidential client

1. should only send signed authentication requests as defined in [@!CIBA] 7.1.1 to the backchannel authentication endpoint.

##NOTE:## When used with FAPI 2.0, both signed and unsigned requests are supported.

### Extensions to CIBA authentication request

This profile defines the following extensions to the authentication request defined in [@!CIBA] Section 7.1.

1. `request_context`: OPTIONAL. a JSON object (the contents of which are not defined by this specification) containing information to inform fraud and threat decisions. For example, an ecosystem may require relying parties to provide geolocation for the consumption device.

## Accessing protected resources

The benefit of the CIBA specification is that once tokens are issued they can be used
in the same manner as tokens issued via authorization code flows.

When this profile is used with the FAPI 1.0 specifications, the provisions for accessing
protected resources detailed in [@!FAPI1.1] and [@!FAPI1.2] apply fully.

When this profile is used with the FAPI 2.0 specifications, the provisions for accessing
protected resources detailed in [@!FAPI2] apply fully.

### Client provisions

In situations where the client does not control the consumption device, the client

1. shall not send `x-fapi-customer-ip-address` or `x-fapi-auth-date` headers; and
1. should send metadata about the consumption device, for example geolocation and device type.

## Registration and discovery metadata

This specification adds additional metadata parameters for OAuth authorization server
metadata as defined in [RFC8414] and dynamic client registration metadata as defined
in [RFC7591].

OAuth authorization server metadata:

1. `backchannel_endpoint_login_hint_token_types_supported`: OPTIONAL. JSON array of strings
   that the authorization server can use to advertise which types of `login_hint_token` it supports. The values
   in this parameter are likely to be ecosystem specific.

Dynamic client registration metadata:

1. `backchannel_endpoint_login_hint_token_types`: OPTIONAL. JSON array of strings that the client can use to register the type of `login_hint_token` that it will use.

# Security considerations

## Introduction

The [@!CIBA] specification introduces some new attack vectors not present in OAuth 2 
redirect based flows. This profile aims to help implementers of [@!CIBA] for 
higher security needs to reduce or eliminate these attack vectors. There are 
however further security considerations that should be taken into account when 
implementing this specification.

It is strongly recommended to use OAuth 2 redirect based flows secured by [@!FAPI1.1], 
[@!FAPI1.2] or [@!FAPI2] for the same device use cases because decoupled flows suffer from session 
binding limitations that are not present in redirect flows. This specification 
is designed to cater for cross device and user not present scenarios. 

## Authentication sessions started without a users knowledge or consent

As this specification allows the client to initiate an authentication request it is
important for the authorization server to know whether the user is aware and has consented
to the authentication process. If widely known user identifiers (e.g. phone numbers) are
used as the `login_hint` in the authentication request then this risk is worsened.
An attacker could start unsolicited authentication sessions on large numbers of authentication
devices, causing distress and potentially enabling fraud.

For this reason this profile highly recommends `login_hint` to have the properties of a
nonce with the expectation being that it will be generated from an authorization server
owned client authentication device. Given the high levels of friction that this may impose
it's anticipated that authorization servers may have to accept an `id_token_hint` as an
alternative mechanism for client subject identification.

If a client wishes to store the `id_token` returned from an authorization server for later
use as an `id_token_hint`, care must be taken to ensure that the customer identification
mechanism used to retrieve the `id_token` is appropriate for the channel being used.

For illustration a QR code on a 'club card' may be an appropriate identifier when using
a POS terminal under CCTV but it might not be an appropriate identifier when used in online ecommerce.

In addition, [@!CIBA] provides an optional `user_code` mechanism to specifically mitigate
this issue, it may be appropriate to require the use of `user_code` in certain deployments.

## Reliance on user to confirm binding messages

Depending on the hint used to identify the user and the client's user authentication
processes, it may be possible for a fraudster to start a malicious [@!CIBA] flow at the
same time as a genuine flow, with both flows using the genuine user’s identifier. If
the scope of access requested is similar then the only way to ensure that a user is
authorizing the correct transaction is for the user to compare the binding messages
on the authentication and consumption devices.

If this risk is deemed unacceptable then implementers should either consider alternative
mechanisms of verifying the binding message (e.g. conveying it to the authentication
device via a QR code), or use ephemeral user identifiers generated on the authentication
device.

## Loss of fraud markers to authorization server

In a redirect-based flow, the authorization server can collect useful fraud markers from
the user-agent. In a [@!CIBA] flow the separation of consumption and authentication devices
reduces the data that can be collected. This could reduce the effectiveness of any fraud
detection system.

## Incomplete or incorrect implementations of the specifications

To achieve the full security benefits, it is important the implementation of this
specification, and the underlying OpenID Connect and OAuth 2.0 specifications, are both
complete and correct.

The OpenID Foundation provides tools that can be used to confirm that an implementation
is correct:

https://openid.net/certification/

The OpenID Foundation maintains a list of certified implementations:

https://openid.net/developers/certified/

Deployments that use this specification should use a certified implementation.

## JWS/JWE Algorithm considerations

When this profile is used with the FAPI 1.0 specifications, authorization servers and clients
shall follow the guidance around JWT signing and encryption algorithms in [@!FAPI1.2] 8.6 and
8.6.1.

When this profile is used with the FAPI 2.0 specifications, authorization servers and clients
shall follow the guidance around cryptography and secrets in [@!FAPI2] 5.4.

## Authentication device security

This profile and the underlying specifications do not specify how the authorization server
should initiate and perform user authentication and authorization of consent on the
authentication device.

Implementors must use appropriately strong methods to communicate with the authentication
device and to authenticate the end user.

## CIBA token delivery modes

[@!CIBA] defines 3 ways that tokens can be delivered to the client.

The `push` mode is not permitted by this specification as it delivers tokens to the
client by calling an endpoint owned by the client. This substantially differs from the
established pattern of retrieving tokens by presenting client authentication to the
token endpoint, and it may have security concerns that are currently unknown.

The `poll` and `ping` modes both follow the established convention of retrieving
tokens from the token endpoint and hence do not have this concern.

The `ping` mode delivers a notification to an endpoint owned by the client. The information
contained in this notification is limited to the `auth_req_id` for the request, as described
in [@!CIBA] 10.2. The bearer token used by the authorization server to access this resource
is not sender constrained. If the `backchannel_client_notification_endpoint`, the
`auth_req_id` and the `client_notification_token` are known to an attacker, they may be able
to force the client to call the token endpoint repeatedly or before the authentication has
completed. For most deployments this is not a significant issue.

## TLS considerations

As confidential information is being exchanged, all interactions shall be encrypted
with TLS (HTTPS).

The recommendations for Secure Use of Transport Layer Security in [@!BCP195] shall be followed,
with the following additional requirements:

1. TLS version 1.2 or later shall be used for all communications.
1. A TLS server certificate check shall be performed, as per [RFC6125].
1. Only the cipher suites recommended in [@!BCP195] shall be permitted.

## Algorithm considerations

For JWS, both clients and authorization servers:

1. shall use `PS256` or `ES256` algorithms;
1. should not use algorithms that use RSASSA-PKCS1-v1_5 (e.g. `RS256`);
1. shall not use `none`;

## Encryption algorithm considerations

For JWE, both clients and authorization servers

1. shall not use the `RSA1_5` algorithm.

# Privacy considerations

There are no additional privacy considerations beyond those in [@!CIBA] 15.

# Acknowledgement

The following people contributed heavily towards this document:

- Nat Sakimura (Nomura Research Institute) -- Chair, Editor
- Anoop Saxana (Intuit) -- Co-chair, FS-ISAC Liaison
- Anthony Nadalin (Microsoft) -- Co-chair, SC 27 Liaison
- Edmund Jay (Illumila) -- Co-editor
- Dave Tonge (Moneyhub) -- Co-chair, UK Implementation Entity Liaison
- Brian Campbell (Ping Identity)
- John Bradley (Yubico)
- Henrik Biering (Peercraft)
- Axel Nennker (Deutsche Telekom)
- Ralph Bragg (RAiDiAM)
- Joseph Heenan (Authlete)
- Torsten Lodderstedt (yes.com)
- Takahiko Kawasaki (Authlete)

# IANA Considerations

## OAuth authorization server metadata registration

This specification adds the following values to the IANA "OAuth Authorization Server Metadata" registry
established by [RFC8414]:

- Server Metadata Name: backchannel_endpoint_login_hint_token_types_supported
- Server Metadata Description: Supported CIBA login hint token types.
- Change Controller: OpenID Foundation Financial-Grade API Working Group - openid-specs-fapi@lists.openid.net
- Specification Document(s): Section 7 of [[this specification]]

## OAuth dynamic client registration metadata registration

This specification requests registration of the following client metadata definitions in the
IANA "OAuth Dynamic Client Registration Metadata" registry established by [RFC7591]:

- Client Metadata Name: backchannel_endpoint_login_hint_token_types
- Client Metadata Description: The supported CIBA login hint token types that the client will use to initiate CIBA requests.
- Change Controller: OpenID Foundation Financial-Grade API Working Group - openid-specs-fapi@lists.openid.net
- Specification Document(s): Section 7 of [[this specification]]

# Appendix A - Examples

The following are non-normative examples of the FAPI-CIBA requests and responses.

All examples use private_key_jwt client authentication with the following key:

```
{
  "kty": "EC",
  "d": "gM__X2faDsb4s6QLer9h-y4KzLIgwt5Jz2dJi5r64Pc",
  "use": "sig",
  "kid": "thrwqnuer",
  "crv": "P-256",
  "x": "YPczq3aBrd8PjtFsXX_HPZNwnzp89vAGjgQXm4cOgdQ",
  "y": "eqE4OZu0V07qXi9ojhQAeqKndWp0QwUfB3aNp4dYYPQ",
  "alg": "ES256"
}
```

## Signed authentication request with private_key_jwt client authentication

This example includes various optional fields, some of which may not be applicable to some deployments. Line wraps within values are for display purposes only.

```
POST /backchannel-authorization-endpoint HTTP/1.1
Host: server.example.com
Content-Type: application/x-www-form-urlencoded

request=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRocndxbnVl
ciJ9.eyJpc3MiOiIzMDExODMzNzM4MTQ5NzkiLCJhdWQiOiJodHRwczovL3NlcnZ
lci5leGFtcGxlLmNvbS8iLCJpYXQiOjE1NjQ5MDI3MzgsIm5iZiI6MTU2NDkwMjc
zOCwiZXhwIjoxNTY0OTAzMDM4LCJqdGkiOiJBSnhaUnBOcWxnNjJVVGR5MzdndSI
sInNjb3BlIjoib3BlbmlkIHBheW1lbnRzIiwiYWNyX3ZhbHVlcyI6InVybjptYWN
lOmluY29tbW9uOmlhcDpzaWx2ZXIgdXJuOm1hY2U6aW5jb21tb246aWFwOmJyb25
6ZSIsImNsaWVudF9ub3RpZmljYXRpb25fdG9rZW4iOiJfTWlVT1kwN0VPQ3ZXUjV
CVnVPTD0iLCJsb2dpbl9oaW50Ijoiam9obkBleGFtcGxlLmNvbSIsImJpbmRpbmd
fbWVzc2FnZSI6IlMyNFIiLCJ1c2VyX2NvZGUiOiI2MzY1IiwicmVxdWVzdGVkX2V
4cGlyeSI6IjEyMCIsInJlcXVlc3RfY29udGV4dCI6eyJsb2NhdGlvbiI6eyJsYXQ
iOjUxLjE3Mzk3LCJsbmciOi0xLjgyMjM4fX0sInBheW1lbnRfaW50ZW50Ijp7ImF
tb3VudCI6IjE2NS44OCIsImN1cnJlbmN5IjoiR0JQIiwiY3JlZGl0b3JfYWNjb3V
udCI6eyJzY2hlbWVfbmFtZSI6IlVLLk9CSUUuU29ydENvZGVBY2NvdW50TnVtYmV
yIiwiaWRlbnRpZmljYXRpb24iOiIwODA4MDAyMTMyNTY5OCIsIm5hbWUiOiJBQ01
FIEluYyJ9fX0.6YQ2j27lXlsfw5QFUoDDbkXJnu8ldi6Tw8LwUEg_C1w2ru_tksY
yIN81jv4Q0NXwRBtWsojahPFynZJa39Q3Yg&
client_assertion=eyJraWQiOiJ0aHJ3cW51ZXIiLCJhbGciOiJFUzI1NiJ9.ey
JzdWIiOiIzMDExODMzNzM4MTQ5NzkiLCJhdWQiOiJodHRwczovL3NlcnZlci5leG
FtcGxlLmNvbS8iLCJpc3MiOiIzMDExODMzNzM4MTQ5NzkiLCJleHAiOjE1NjQ5MD
I3OTgsImlhdCI6MTU2NDkwMjczOCwianRpIjoiNnNSVndWdVpseDFERUJjSEVIaH
gifQ.b9fpM3hUv5Nex9DZOYS8AGUiBMIFnlvf5YgRmUqzBhljIGr4M5f-mkt2VOM
ImaKe-LaUMeD5y_PZGaBiDTo50A&
client_assertion_type=urn%3Aietf%3Aparams%3Aoauth%3Aclient-asser
tion-type%3Ajwt-bearer
```

which contains the JWT payload:

```
{
  "iss": "301183373814979",
  "aud": "https://server.example.com/",
  "iat": 1564902738,
  "nbf": 1564902738,
  "exp": 1564903038,
  "jti": "AJxZRpNqlg62UTdy37gu",
  "scope": "openid payments",
  "acr_values": "urn:mace:incommon:iap:silver urn:mace:incommon:iap:bronze",
  "client_notification_token": "_MiUOY07EOCvWR5BVuOL=",
  "login_hint": "john@example.com",
  "binding_message": "S24R",
  "user_code": "6365",
  "requested_expiry": "120",
  "request_context": {
    "location": {
      "lat": 51.17397,
      "lng": -1.82238
    }
  },
  "payment_intent": {
    "amount": "165.88",
    "currency": "GBP",
    "creditor_account": {
      "scheme_name": "UK.OBIE.SortCodeAccountNumber",
      "identification": "08080021325698",
      "name": "ACME Inc"
    }
  }
}
```

{backmatter}

<reference anchor="FAPI2" target="https://openid.net/specs/fapi-2_0-security-profile-ID2.html">
  <front>
    <title>FAPI 2.0 Security Profile</title>
    <author initials="D." surname="Fett" fullname="Daniel Fett">
      <organization>yes.com</organization>
    </author>
  <date day="25" month="February" year="2014" />

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

<reference anchor="CIBA" target="http://openid.net/specs/openid-client-initiated-backchannel-authentication-core-1_0.html">
    <front>
        <title>OpenID Connect Client Initiated Backchannel Authentication Core</title>
        <author initials="D." surname="Fett" fullname="Daniel Fett">
      <organization>yes.com</organization>
    </author>
      <date day="25" month="February" year="2014" />
    </front>

</reference>

<reference anchor="FAPI1.1" target="https://openid.net/specs/openid-financial-api-part-1.html">
    <front>
        <title>FAPI Part 1: Baseline Security Profile</title>
        <author initials="D." surname="Fett" fullname="Daniel Fett">
      <organization>yes.com</organization>
    </author>
        <date day="25" month="February" year="2014" />
    </front>


</reference>

<reference anchor="FAPI1.2" target="https://openid.net/specs/openid-financial-api-part-2.html">
    <front>
        <title>FAPI Part 2: Advanced Security Profile</title>
        <author initials="D." surname="Fett" fullname="Daniel Fett">
      <organization>yes.com</organization>
    </author>
        <date day="25" month="February" year="2014" />
    </front>


</reference>

<reference anchor="RAR" target="https://datatracker.ietf.org/doc/html/draft-ietf-oauth-rar">
    <front>
        <title>OAuth 2.0 Rich Authorization Requests</title>
        <author initials="D." surname="Fett" fullname="Daniel Fett">
      <organization>yes.com</organization>
    </author>
          <date day="25" month="February" year="2014" />
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

Copyright (c) 2024 The OpenID Foundation.

The OpenID Foundation (OIDF) grants to any Contributor, developer, implementer, or other interested party a non-exclusive, royalty free, worldwide copyright license to reproduce, prepare derivative works from, distribute, perform and display, this Implementers Draft or Final Specification solely for the purposes of (i) developing specifications, and (ii) implementing Implementers Drafts and Final Specifications based on such documents, provided that attribution be made to the OIDF as the source of the material, but that such attribution does not indicate an endorsement by the OIDF.

The technology described in this specification was made available from contributions from various sources, including members of the OpenID Foundation and others. Although the OpenID Foundation has taken steps to help ensure that the technology is available for distribution, it takes no position regarding the validity or scope of any intellectual property or other rights that might be claimed to pertain to the implementation or use of the technology described in this specification or the extent to which any license under such rights might or might not be available; neither does it represent that it has made any independent effort to identify any such rights. The OpenID Foundation and the contributors to this specification make no (and hereby expressly disclaim any) warranties (express, implied, or otherwise), including implied warranties of merchantability, non-infringement, fitness for a particular purpose, or title, related to this specification, and the entire risk as to implementing this specification is assumed by the implementer. The OpenID Intellectual Property Rights policy requires contributors to offer a patent promise not to assert certain patent claims against other contributors and against implementers. The OpenID Foundation invites any interested party to bring to its attention any copyrights, patents, patent applications, or other proprietary rights that may cover technology that may be required to practice this specification.
