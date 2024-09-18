%%%
title = "FAPI 2.0 Http Signatures (Draft)"
abbrev = "fapi-2-http-signatures"
ipr = "none"
workgroup = "fapi"
keyword = ["security", "openid"]

[seriesInfo]
name = "Internet-Draft"
value = "fapi-2_0-http-signatures-01"
status = "standard"

[[author]]
initials="D."
surname="Tonge"
fullname="Dave Tonge"
organization="Moneyhub Financial Technology"
    [author.address]
    email = "dave@tonge.org"
 
[[author]]
initials="D."
surname="Fett"
fullname="Daniel Fett"
organization="Authlete"
    [author.address]
    email = "mail@danielfett.de"

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

Final drafts adopted by the Workgroup through consensus are circulated publicly for the public review for 60 days and for the OIDF members for voting. Publication as an OIDF Standard requires approval by at least 50% of the members casting a vote. There is a possibility that some of the elements of this document may be the subject to patent rights. OIDF shall not be held responsible for identifying any or all such patent rights.


.# Introduction

OIDF FAPI 2.0 is an API security profile based on the OAuth 2.0 Authorization
Framework [@!RFC6749]. This HTTP Signature Profile is part of the FAPI 2.0 family of specifications with a focus on providing interoperable support for non-repudiation across HTTP requests and responses. 

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

This document specifies the methods for clients, authorization servers and resource servers to sign and verify messages.

# Normative references

The following documents are referred to in the text in such a way that some or all of their content constitutes requirements of this document. For dated references, only the edition cited applies. For undated references, the latest edition of the referenced document (including any amendments) applies.

See Clause 8 for normative references.

# Terms and definitions

For the purpose of this document, the terms defined in [@!RFC6749], [@!RFC6750], [@!RFC7636], [@!OIDC] and [@!ISO29100] apply.

# Symbols and Abbreviated terms

**API** – Application Programming Interface

**HTTP** – Hyper Text Transfer Protocol

**JAR** – JWT-Secured Authorization Request

**JARM** – JWT Secured Authorization Response Mode

**JWT** – JSON Web Token

**JSON** – JavaScript Object Notation

**OIDF** – OpenID Foundation

**PAR** – Pushed Authorization Requests

**PKCE** – Proof Key for Code Exchange

**REST** – Representational State Transfer

**TLS** – Transport Layer Security

**URI** – Uniform Resource Identifier

**URL** – Uniform Resource Locator

# HTTP signature profile

OIDF FAPI 2.0 is an API security profile based on the OAuth 2.0 Authorization
Framework [@!RFC6749]. This HTTP signature profile aims to reach the security goals
laid out in the Attacker Model [@!attackermodel] plus the non-repudiation goals listed below.

TODO: Add in reference to Message Signing spec

## Profile

In addition to the technologies used in the [@!FAPI2_Security_Profile_ID2], the
following standards are used in this profile:

  * HTTP Message Signatures [@!RFC9421] and Digest Fields [@!RFC9530]
  for signing HTTP requests to and responses from resource servers.


## Non-repudiation

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
  
  * NR5: resource requests
  * NR6: resource responses

## HTTP message signing

To support non-repudiation for NR5 and NR6, HTTP requests, responses, or both can be signed.

### Requirements for signing and verifying resource requests

#### Clients

Clients sending signed resource requests act in the role of "signer" as defined by 
[@!RFC9421]. This signer

1. shall create an HTTP message signature as described in [@!RFC9421];
1. shall include `@method` (the method used in the HTTP request) in the signature;
1. shall include `@target-uri` (the full request URI of the HTTP request) in the signature;
1. shall include the `created` parameter (the signature creation time) in the signature;
1. shall include the `tag` parameter with a value of `fapi-2-request` in the signature;
1. shall include the `Authorization` header in the signature;
1. when DPoP [@!RFC9449] is in use, shall include the `DPoP` header in the signature;
1. when the message contains a request body, shall include the `content-digest` header as defined in 
    [@I-D.ietf-httpbis-digest-headers] in the request, shall include that header in the signature, and should use 
    content-encoding agnostic digest methods (such as sha-256).
 
#### Resource servers 

Resource servers receiving signed resource requests act in the role of "verifier" as 
defined by [@!RFC9421]. This verifier

1. shall retrieve the valid public key for the client;
1. shall verify the signature received from the client as described in [@!RFC9421];
1. shall reject requests with missing or invalid signatures using HTTP status code 401;
1. shall reject requests which don't have a tag parameter with the value of `fapi-2-request` in the signature;
1. shall reject requests with signatures that are missing `@method`, `@target-uri`, or `Authorization` in the signature;
1. shall reject requests with signatures that are missing the `created` parameter or have a `created` value 
   that is greater than an acceptable range (1 minute is recommended);
1. when a `DPoP` header is present in the request, shall reject requests that are missing `DPoP` in the signature;
1. when the request contains a request body, shall reject requests that are missing `content-digest` in the signature.


**NOTE:** This specification doesn't specify the exact means by which a resource server can retrieve
the key for the client. The resource server can obtain an identifier for the client either from a 
mutual TLS cerficiate or from a JWT access token or from a token introspection response. With a client
identifier and the `keyid` in the `Signature-Input` field, the resource server can retrieve the key from 
a trusted third party or by some other means.
 
 
### Requirements for signing and verifying resource responses

#### Resource servers 

Resource servers responding with a signed resource response act in the role of "signer" as defined 
by [@!RFC9421]. This signer

1. shall create an HTTP message signature for the response as described in [@!RFC9421];
1. shall cryptographically link the response to the request by including the request method, request target-uri and 
(if applicable) the request content-digest in the response signature input by means of the `req` boolean flag defined 
in Section 2.4 of [@!RFC9421];
1. if the request was signed, shall include the request signature and request signature input in the response 
signature input by means of the `req` boolean flag defined in Section 2.4 of [@!RFC9421]; 
1. shall include `@status` (the status code of the response) in the signature;
1. shall include the `created` parameter (the signature creation time) in the signature;
1. shall include the `tag` parameter with a value of `fapi-2-response` in the signature;
1. when the response contains a response body, shall include the `content-digest` header as defined in [@!RFC9530] 
in the response, and shall include that header in the signature, and should use content-encoding agnostic digest methods (such as sha-256). 

**NOTE:** In order to cryptographically link a response to a signed request, it is not sufficient to sign only the request signature value. Instead, the server has to sign all portions of the request relevant to generating the response by using the req feature of the HTTP message signature generation. This specification mandates a minimum coverage, but signers are required to sign anything else relevant to the API being protected, including headers and contents.
 
 
#### Clients

Clients receiving signed resource responses act in the role of "verifier" as 
defined by [@!RFC9421]. This verifier

1. shall retrieve the valid public key for the resource server;
1. shall accept and verify the signature in the response as described in [@!RFC9421];
1. shall verify that `@status` and `created` are included in the signature;
1. if the response contains a body, shall verify that `content-digest` is in the signature; and
1. shall verify that the signature contains the tag parameter with a value of `fapi-2-response`.

 
**NOTE:** This specification doesn't specify the exact means by which a client can retrieve
the key for the resource server. Together with the identity of the resource server and the 
`keyid` in the `Signature-Input` field, the client can retrieve the key from a trusted third 
party or by some other means. 

**NOTE:** As noted in Section 2.4 of [@!RFC9421], the client will need to 
keep data related to the request in order to verify the response signature.


# Security considerations

## Difficulty in linking a signed message to a real world identity

This specification provides the technical means to sign messages, however proving that a specific signed response is
linked to a specific real world end-user, or that a real world end-user initiated a specific request is outside of the
scope of this document.



# Privacy considerations

In addition to the privacy considerations detailed in [@!FAPI2_Security_Profile_ID2] implementers should consider
the privacy implications of storing messages for the purpose of non-repudiation. 

Such messages may well contain personally identifiable information and implementers should evaluate 
whether such messages need to be stored. If they are stored then adequate access controls must be 
put in place to protect that data. Such controls should follow data minimisation principles and ensure that 
there are tamper-proof audit logs.

# Acknowledgements

This specification was developed by the OpenID FAPI Working Group. 

We would like to thank Takahiko Kawasaki, Filip Skokan, Nat Sakimura, Dima Postnikov, Brian Campbell, Ralph Bragg, Justin Richer and Lukasz Jaromin for their valuable feedback and contributions that helped to evolve this specification.


{backmatter}

<reference anchor="FAPI2_Security_Profile_ID2" target="https://openid.net/specs/fapi-2_0-security-profile-ID2.html">
  <front>
    <title>FAPI 2.0 Security Profile</title>
    <author initials="D." surname="Fett" fullname="Daniel Fett">
      <organization>Authlete</organization>
    </author>
   <date day="7" month="Dec" year="2022"/>
  </front>
</reference>

<reference anchor="attackermodel" target="https://openid.net/specs/fapi-2_0-attacker-model-ID2.html">
  <front>
    <title>FAPI 2.0 Attacker Model</title>
    <author initials="D." surname="Fett" fullname="Daniel Fett">
      <organization>Authlete</organization>
    </author>
   <date day="7" month="Dec" year="2022"/>
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

# Notices

Copyright (c) 2024 The OpenID Foundation.

The OpenID Foundation (OIDF) grants to any Contributor, developer, implementer, or other interested party a non-exclusive, royalty free, worldwide copyright license to reproduce, prepare derivative works from, distribute, perform and display, this Implementers Draft or Final Specification solely for the purposes of (i) developing specifications, and (ii) implementing Implementers Drafts and Final Specifications based on such documents, provided that attribution be made to the OIDF as the source of the material, but that such attribution does not indicate an endorsement by the OIDF.

The technology described in this specification was made available from contributions from various sources, including members of the OpenID Foundation and others. Although the OpenID Foundation has taken steps to help ensure that the technology is available for distribution, it takes no position regarding the validity or scope of any intellectual property or other rights that might be claimed to pertain to the implementation or use of the technology described in this specification or the extent to which any license under such rights might or might not be available; neither does it represent that it has made any independent effort to identify any such rights. The OpenID Foundation and the contributors to this specification make no (and hereby expressly disclaim any) warranties (express, implied, or otherwise), including implied warranties of merchantability, non-infringement, fitness for a particular purpose, or title, related to this specification, and the entire risk as to implementing this specification is assumed by the implementer. The OpenID Intellectual Property Rights policy requires contributors to offer a patent promise not to assert certain patent claims against other contributors and against implementers. The OpenID Foundation invites any interested party to bring to its attention any copyrights, patents, patent applications, or other proprietary rights that may cover technology that may be required to practice this specification.
