%%%
title = "FAPI 2.0 Message Signing"
abbrev = "fapi-2-message-signing"
ipr = "none"
workgroup = "fapi"
keyword = ["security", "openid"]

[seriesInfo]
name = "Internet-Draft"
value = "fapi-2_0-message-signing-01"
status = "standard"
 
[[author]]
initials="D."
surname="Fett"
fullname="Daniel Fett"
organization="yes.com"
    [author.address]
    email = "mail@danielfett.de"

[[author]]
initials="D."
surname="Tonge"
fullname="Dave Tonge"
organization="Moneyhub Financial Technology"
    [author.address]
    email = "dave@tonge.org"


[[contact]]
fullname="Takahiko Kawasaki"

[[contact]]
fullname="Filip Skokan"

[[contact]]
fullname="Nat Sakimura"

[[contact]]
fullname="Dima Postnikov"

[[contact]]
fullname="Joseph Heenan"

[[contact]]
fullname="Brian Campbell"

[[contact]]
fullname="Ralph Bragg"

[[contact]]
fullname="Lukasz Jaromin"

[[contact]]
fullname="Justin Richer"

%%%

.# Abstract 

OIDF FAPI 2.0 is an API security profile based on the OAuth 2.0
Authorization Framework [@!RFC6749].

{mainmatter}

# Introduction

## Warning

This document is not an OIDF International Standard. It is distributed
for review and comment. It is subject to change without notice and may
not be referred to as an International Standard.

Recipients of this draft are invited to submit, with their comments,
notification of any relevant patent rights of which they are aware and
to provide supporting documentation.

## Copyright notice & license

The OpenID Foundation (OIDF) grants to any Contributor, developer,
implementer, or other interested party a non-exclusive, royalty free,
worldwide copyright license to reproduce, prepare derivative works
from, distribute, perform and display, this Implementers Draft or
Final Specification solely for the purposes of (i) developing
specifications, and (ii) implementing Implementers Drafts and Final
Specifications based on such documents, provided that attribution be
made to the OIDF as the source of the material, but that such
attribution does not indicate an endorsement by the OIDF.

The technology described in this specification was made available from
contributions from various sources, including members of the OpenID
Foundation and others. Although the OpenID Foundation has taken steps
to help ensure that the technology is available for distribution, it
takes no position regarding the validity or scope of any intellectual
property or other rights that might be claimed to pertain to the
implementation or use of the technology described in this
specification or the extent to which any license under such rights
might or might not be available; neither does it represent that it has
made any independent effort to identify any such rights. The OpenID
Foundation and the contributors to this specification make no (and
hereby expressly disclaim any) warranties (express, implied, or
otherwise), including implied warranties of merchantability,
non-infringement, fitness for a particular purpose, or title, related
to this specification, and the entire risk as to implementing this
specification is assumed by the implementer. The OpenID Intellectual
Property Rights policy requires contributors to offer a patent promise
not to assert certain patent claims against other contributors and
against implementers. The OpenID Foundation invites any interested
party to bring to its attention any copyrights, patents, patent
applications, or other proprietary rights that may cover technology
that may be required to practice this specification.


## Notational Conventions

The keywords "shall", "shall not",
"should", "should not", "may", and
"can" in this document are to be interpreted as described in
ISO Directive Part 2 [@!ISODIR2].
These keywords are not used as dictionary terms such that
any occurrence of them shall be interpreted as keywords
and are not to be interpreted with their natural language meanings.
# Message Signing Profile

OIDF FAPI 2.0 is an API security profile based on the OAuth 2.0 Authorization
Framework [@!RFC6749]. This Message Signing Profile aims to reach the security goals
laid out in the Attacker Model [@!attackermodel] plus the non-repudiation goals listed below.

All provisions of the [@!FAPI2_Security_Profile_ID2] apply to the Message Signing Profile
as well, with the extensions described in the following.


## Profile

In addition to the technologies used in the [@!FAPI2_Security_Profile_ID2], the
following standards are used in this profile:

  * OAuth 2.0 JWT Secured Authorization Request (JAR) [@!RFC9101] for signing authorization requests
  * JWT Secured Authorization Response Mode for OAuth 2.0 [@!JARM] for signing authorization responses 
  * OAuth 2.0 Token Introspection [@!RFC7662] with [@I-D.ietf-oauth-jwt-introspection-response] for signing introspection responses
  * HTTP Message Signatures [@I-D.ietf-httpbis-message-signatures] and Digest Fields [@I-D.ietf-httpbis-digest-headers]
  for signing HTTP requests to and responses from Resource Servers.

We understand that some ecosystems may only desire to implement 1 or 2 of the above 3, it is therefore 
anticipated that a piece of software will be able to conform to each of the methods separately, i.e. there
will be separate test options for each of the following:

 * Signed Authorization Requests
 * Signed Authorization Responses
 * Signed Introspection Responses
 * Signed HTTP Messages


## Non-Repudiation

Beyond what is captured by the security goals and the attacker model in
[@!attackermodel], parties could try to deny having sent a particular message,
for example, a payment request. For this purpose, non-repudiation is needed.

In the context of this specification, non-repudiation refers to the assurance that the owner of 
a signature key pair that was capable of generating an existing signature corresponding to certain 
data cannot convincingly deny having signed the data ([@!NIST.SP.800-133]).

This is usually achieved by providing application-level signatures that can be
stored together with the payload and meaningful metadata of a request or
response. 

The following messages are affected by this specification:

  * NR1: Pushed Authorization Requests
  * NR2: Authorization Requests (Front-Channel)
  * NR3: Authorization Responses (Front-Channel)  
  * NR4: Introspection Responses
  * NR5: Resource Requests
  * NR6: Resource Responses

## Signing Authorization Requests

To support non-repudiation for NR1, Pushed Authorization Requests can be signed. 
Because FAPI2 uses [@!RFC9126], NR2 is achieved by default when the Pushed Authorization request
is signed.


### Requirements for Authorization Servers

Authorization servers implementing FAPI2 authorization request signing

 1. shall support and verify signed request objects according to JAR
    [@!RFC9101] at the PAR endpoint [@!RFC9126]
 2. shall require the aud claim in the request object to be, or to be an array containing, the OP's Issuer Identifier URL;
 3. shall require the request object to contain an `nbf` claim that is no longer than 60 minutes in the past; and
 4. shall require the request object to contain an `exp` claim that has a lifetime of no longer than 60 minutes after the `nbf` claim;

### Requirements for Clients

Clients implementing FAPI2 authorization request signing

 1. shall sign request objects according to JAR [@!RFC9101] that are sent to the PAR 
    endpoint [@!RFC9126]
 2. shall send the `aud` claim in the request object as the OP's Issuer Identifier URL;
 3. shall send a `nbf` claim in the request object;
 4. shall send an `exp` claim in the request object that has a lifetime of no longer than 60 minutes;
 
## Signing Authorization Responses

To support non-repudiation for NR3, Authorization Responses can be signed. 

### Requirements for Authorization Servers

Authorization servers implementing FAPI2 authorization response signing

 1. shall support and issue signed authorization responses via JWT Secured Authorization 
    Response Mode for OAuth 2.0 [@!JARM]

**NOTE**: When using [@!JARM] an Authorization Server should only include the iss authorization response 
parameter defined by [@!RFC9207] inside the JWT. This is because [@!RFC9207] defines `iss` 
to be an authorization response parameter, and [@!JARM] section 4.1 requires all authorization 
response parameters to be inside the JWT.

### Requirements for Clients

Clients implementing FAPI2 authorization response signing

 1. shall set the `response_mode` to `jwt` in the authorization request as defined in [@!JARM]
 2. shall verify signed authorization responses according to [@!JARM]


## Signing Introspection Responses

To support non-repudiation for NR4, Introspection Responses can be signed.

### Requirements for Authorization Servers

Authorization servers implementing FAPI2 introspection response signing

 1. shall sign introspection responses that are issued in JWT format according to [@!I-D.ietf-oauth-jwt-introspection-response]
 
### Requirements for Clients

Clients implementing FAPI2 introspection response signing

 1. shall request signed token introspection responses according to [@!I-D.ietf-oauth-jwt-introspection-response] 
 2. shall verify the signed token introspection responses


## HTTP Message Signing

To support non-repudiation for NR5 and NR6, HTTP requests and responses
can be signed.

This profile supports HTTP Message Signing using the *HTTP Message Signatures* specification
being developed by the IETF HTTP Working Group.


### Requirements for signing and verifying resource requests

#### Clients

Clients sending signed resource requests act in the role of "signer" as defined by 
[@I-D.ietf-httpbis-message-signatures]. The signer has the following requirements:

1. shall create an HTTP Message Signature as described in [@!I-D.ietf-httpbis-message-signatures]
1. shall include `@method` (the method used in the HTTP request) in the signature
1. shall include `@target-uri` (the full request URI of the HTTP request) in the signature
1. shall include the `created` parameter (the signature creation time) in the signature
1. shall include the `tag` parameter with a value of `fapi-2-request` in the signature
1. shall include the `Authorization` header in the signature
1. when DPoP is in use, shall include the `DPoP` header in the signature
1. when the message contains a request body, shall include the `content-digest` header as defined in 
    [@I-D.ietf-httpbis-digest-headers] in the request, and include that header in the signature.
    Content-encoding agnostic digest methods (such as sha-256) should be used.
 
#### Resource Servers 

Resource servers receiving signed resource requests act in the role of "verifier" as 
defined by [@!I-D.ietf-httpbis-message-signatures]. The verifier has the following requirements:

1. shall retrieve the valid public key for the client
1. shall verify the signature received from the Client as described in [@!I-D.ietf-httpbis-message-signatures].
1. shall reject requests with missing or invalid signatures using HTTP Status Code 401
1. shall reject requests which don't have a tag parameter with the value of `fapi-2-request` in the signature
1. shall reject requests with signatures that are missing `@method`, `@target-uri`, or `Authorization` in the signature
1. shall reject requests with signatures that are missing the `created` parameter or have a `created` value 
   that is greater than an acceptable range. (1 minute is recommended)
1. when a `DPoP` header is present in the request, shall reject requests that are missing `DPoP` in the signature
1. when the request contains a request body, shall reject requests that are missing `content-digest` in the signature


**NOTE:** This specification doesn't specify the exact means by which a Resource Server can retrieve
the key for the Client. The Resource Server can obtain an identifier for the Client either from a 
mutual TLS cerficiate or from a JWT access token or from a token introspection response. With a Client
identifier and the `keyid` in the `Signature-Input` field, the Resource Server can retrieve the key from 
a trusted third party or by some other means.
 
 
### Requirements for signing and verifying resource responses

#### Resource Servers 

Resource servers responding with a signed resource response act in the role of "signer" as defined 
by [@!I-D.ietf-httpbis-message-signatures]. The signer has the following requirements:

1. shall create an HTTP Message Signature for the response as described in [@!I-D.ietf-httpbis-message-signatures].
1. shall cryptographically link the response to the request by including the request signature in the response signature input by means of the `req` boolean flag defined in 2.4 in [@!I-D.ietf-httpbis-message-signatures] on the signature field  of the request that caused the response
1. shall include `@status` (the status code of the response) in the signature
1. shall include the `created` parameter (the signature creation time) in the signature
1. shall include the `tag` parameter with a value of `fapi-2-response` in the signature
1. when the response contains a response body, shall include the `content-digest` header as defined in 
    [@!I-D.ietf-httpbis-digest-headers] in the response, and include that header in the signature. Content-encoding agnostic digest methods (such as sha-256) should be used. 

 
#### Clients

Clients receiving signed resource responses act in the role of "verifier" as 
defined by [@!I-D.ietf-httpbis-message-signatures]. The verifier has the following requirements:

1. shall retrieve the valid public key for the Resource Server.
1. shall accept and verify the signature in the response as described in [@!I-D.ietf-httpbis-message-signatures]
1. shall verify that `@status` and `created` are included in the signature
1. if the response contains a body, shall verify that `content-digest` is in the signature
1. shall verify that the signature contains the tag parameter with a value of `fapi-2-response`

 
**NOTE:** This specification doesn't specify the exact means by which a Client can retrieve
the key for the Resource Server. Together with the identity of the Resource Server and the 
`keyid` in the `Signature-Input` field, the Client can retrieve the key from a trusted third 
party or by some other means. 

**NOTE:** As noted in [@!I-D.ietf-httpbis-message-signatures] section 2.4, the Client will need to 
keep the request signature value in order to verify the response signature.


## MTLS Protection of all endpoints

Some ecosystems are choosing to require clients accessing their endpoints to supply a TLS client certificate at
endpoints that would not otherwise require a TLS client certificate (for example, the PAR endpoint when using
`private_key_jwt` authentication).

This is outside of the scope of both [@!RFC8705] and the FAPI standards, however in the interests of interoperability we
state that when using TLS as a transport level protection in this manner, authorization servers should expect clients to
call the endpoints located in the root of the server metadata, and not those found in `mtls_endpoint_aliases`.

# Security Considerations

## Authorization Response Encryption

In FAPI2, there is no confidential information in the Authorization Response, hence encryption of the Authorization Response is not required for the purposes of security or confidentiality. In addition, to achieve greater interoperability, it is not recommended to use encryption in this case. 

Usage of PKCE in FAPI 2 provides protection for code leakage described in 5.4 [@!JARM].

# Acknowledgements

This specification was developed by the OpenID FAPI Working Group. 


We would like to thank 
[@Ralph Bragg], 
[@Brian Campbell], 
[@Joseph Heenan], 
[@Lukasz Jaromin],
[@Takahiko Kawasaki], 
[@Dima Postnikov], 
[@Justin Richer],
[@Nat Sakimura], and
[@Filip Skokan] 
for their valuable feedback and contributions that helped to evolve this specification.


{backmatter}

<reference anchor="FAPI2_Security_Profile_ID2" target="https://openid.net/specs/fapi-2_0-security-02.html">
  <front>
    <title>FAPI 2.0 Security Profile</title>
    <author initials="D." surname="Fett" fullname="Daniel Fett">
      <organization>yes.com</organization>
    </author>
   <date day="14" month="Nov" year="2022"/>
  </front>
</reference>

<reference anchor="attackermodel" target="https://openid.net/specs/fapi-2_0-attacker-model-02.html">
  <front>
    <title>FAPI 2.0 Attacker Model</title>
    <author initials="D." surname="Fett" fullname="Daniel Fett">
      <organization>yes.com</organization>
    </author>
   <date day="14" month="Nov" year="2022"/>
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

<reference anchor="NIST.SP.800-133" target="https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-133.pdf">
  <front>
    <title>NIST Special Publication 800-133</title>
     <author fullname="Elaine Barker">
      <organization></organization>
    </author>
     <author fullname="Allen Roginsky ">
      <organization></organization>
    </author>
   <date day="23" month="July" year="2019"/>
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

<reference anchor="preload" target="https://hstspreload.org/">
<front>
<title>HSTS Preload List Submission</title>
    <author fullname="Anonymous">
      <organization></organization>
    </author>
</front>
</reference>

